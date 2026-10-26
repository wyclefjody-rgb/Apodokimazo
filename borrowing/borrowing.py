"""
    borrowing: can simple overlap measures tell literary borrowing from shared church language? Rules in
    borrowing/PREDICTIONS.md (SHA-256 35906bca…198e), sections 2-3.

    Part 1, whole letters: rare shared words, shared 4-lemma strings and order, for three calibration pairs of known
    borrowing, the pairs under test (1 Peter with Hebrews, Romans and Ephesians) and every other pair of New
    Testament letters as controls.
    Part 2, passages: Romans 13:1-7 against every 5-verse window of Mark and every 7-verse window of 1 Peter.

    Needs sblgnt/ (MorphGNT). Output: BORROWING.md.

    Usage (from the kit folder):   python -X utf8 borrowing/borrowing.py
"""
import math
import os
import sys
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
SBLGNT = os.path.join(KIT, "sblgnt")
OUTPUT = os.path.join(HERE, "BORROWING.md")

LETTERS = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm", "Heb", "Jas",
           "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jud"]
CALIBRATION = [("2Pe", "Jud"), ("Eph", "Col"), ("2Th", "1Th")]
REFERENCE = [("Mt", "Mk"), ("Lk", "Mk")]
TESTS = [("1Pe", "Heb"), ("1Pe", "Ro"), ("1Pe", "Eph")]
EXCLUDED = [("1Pe", "2Pe"), ("1Ti", "2Ti"), ("1Ti", "Tit"), ("2Ti", "Tit"), ("1Jn", "2Jn"), ("1Jn", "3Jn"),
            ("2Jn", "3Jn"), ("Col", "Phm")]
RARE_LIMIT = 3
STRING = 4
CONTENT_POS = {"N-", "V-", "A-"}
COMMON = {"εἰμί", "λέγω", "γίνομαι"}


def read_nt():
    """Every NT book as a list of verses: (chapter, verse, [(lemma, part of speech)])."""
    books = {}
    for path in sorted(glob(os.path.join(SBLGNT, "*-morphgnt.txt"))):
        book = os.path.basename(path).split("-")[1]
        verses = []
        with open(path, encoding="utf8") as file:
            for line in file:
                columns = line.split()
                chapter = int(columns[0][2:4])
                verse = int(columns[0][4:6])
                if not verses or verses[-1][0] != chapter or verses[-1][1] != verse:
                    verses.append((chapter, verse, []))
                verses[-1][2].append((columns[6], columns[1]))
        books[book] = verses
    if len(books) < 27:
        sys.exit(f"Expected 27 MorphGNT books in '{SBLGNT}', found {len(books)}. Run setup_data.py first.")
    return books


def lemmas_of(verses):
    words = []
    for chapter, verse, tagged in verses:
        for lemma, pos in tagged:
            words.append(lemma)
    return words


def counts_of(words):
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def grams(words, size):
    found = {}
    for index in range(len(words) - size + 1):
        gram = tuple(words[index:index + size])
        if gram not in found:
            found[gram] = index
    return found


def ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    for position, index in enumerate(order):
        result[index] = float(position)
    return result


def spearman(first, second):
    if len(first) < 6:
        return None
    a = ranks(first)
    b = ranks(second)
    mean_a = sum(a) / len(a)
    mean_b = sum(b) / len(b)
    top = 0.0
    left = 0.0
    right = 0.0
    for index in range(len(a)):
        top += (a[index] - mean_a) * (b[index] - mean_b)
        left += (a[index] - mean_a) ** 2
        right += (b[index] - mean_b) ** 2
    if left == 0 or right == 0:
        return None
    return top / math.sqrt(left * right)


def longest_shared(first, second):
    best = 0
    best_words = []
    size = 1
    while True:
        first_grams = grams(first, size)
        second_grams = grams(second, size)
        hit = None
        for gram in first_grams:
            if gram in second_grams:
                hit = gram
                break
        if hit is None:
            break
        best = size
        best_words = list(hit)
        size += 1
    return best, best_words


def compare(books, totals, name_a, name_b):
    first = lemmas_of(books[name_a])
    second = lemmas_of(books[name_b])
    count_a = counts_of(first)
    count_b = counts_of(second)
    shorter = min(len(first), len(second))
    rare = []
    for lemma in count_a:
        if lemma in count_b:
            outside = totals.get(lemma, 0) - count_a[lemma] - count_b[lemma]
            if outside <= RARE_LIMIT:
                rare.append(lemma)
    first_grams = grams(first, STRING)
    second_grams = grams(second, STRING)
    shared = []
    for gram in first_grams:
        if gram in second_grams:
            shared.append(gram)
    positions_a = []
    positions_b = []
    for lemma in rare:
        positions_a.append(first.index(lemma) / len(first))
        positions_b.append(second.index(lemma) / len(second))
    longest, words = longest_shared(first, second)
    return {"pair": f"{name_a}-{name_b}", "shorter": shorter, "rare": rare, "rare_rate": 1000.0 * len(rare) / shorter,
            "strings": shared, "string_rate": 1000.0 * len(shared) / shorter,
            "order": spearman(positions_a, positions_b), "longest": longest, "longest_words": words}


def string_rate_of(result):
    return result["string_rate"]


def same_pair(pair, pairs):
    for a, b in pairs:
        if (pair[0] == a and pair[1] == b) or (pair[0] == b and pair[1] == a):
            return True
    return False


def percentile_of(value, values):
    below = 0
    for other in values:
        if other < value:
            below += 1
    return 100.0 * below / len(values) if values else float("nan")


def content_lemmas(verses):
    found = set()
    for chapter, verse, tagged in verses:
        for lemma, pos in tagged:
            if pos in CONTENT_POS and lemma not in COMMON:
                found.add(lemma)
    return found


def idf_table(books):
    containing = {}
    total = 0
    for verses in books.values():
        for chapter, verse, tagged in verses:
            total += 1
            seen = set()
            for lemma, pos in tagged:
                seen.add(lemma)
            for lemma in seen:
                containing[lemma] = containing.get(lemma, 0) + 1
    table = {}
    for lemma, count in containing.items():
        table[lemma] = math.log(total / count)
    return table


def passage(books, book, chapter, start, end):
    chosen = []
    for verse in books[book]:
        if verse[0] == chapter and start <= verse[1] <= end:
            chosen.append(verse)
    return chosen


def similarity(first, second, idf):
    shared = content_lemmas(first) & content_lemmas(second)
    score = 0.0
    for lemma in shared:
        score += idf[lemma]
    return score, sorted(shared)


def strings_between(first, second, size):
    a = lemmas_of(first)
    b = lemmas_of(second)
    b_grams = grams(b, size)
    found = []
    for gram in grams(a, size):
        if gram in b_grams:
            found.append(" ".join(gram))
    return found


def windows(books, book, size, target, idf):
    verses = books[book]
    scored = []
    for index in range(len(verses) - size + 1):
        chunk = verses[index:index + size]
        score, shared = similarity(chunk, target, idf)
        label = f"{book} {chunk[0][0]}:{chunk[0][1]}-{chunk[-1][0]}:{chunk[-1][1]}"
        scored.append((score, label, shared, chunk[0][0], chunk[0][1]))
    scored.sort(reverse=True)
    return scored


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    books = read_nt()
    totals = {}
    for verses in books.values():
        for lemma in lemmas_of(verses):
            totals[lemma] = totals.get(lemma, 0) + 1

    controls = []
    for index, a in enumerate(LETTERS):
        for b in LETTERS[index + 1:]:
            pair = (a, b)
            if same_pair(pair, CALIBRATION + TESTS + EXCLUDED):
                continue
            controls.append(compare(books, totals, a, b))

    lines = ["# borrowing: results", "",
             "Rules: PREDICTIONS.md (SHA-256 35906bca28a5a63f40a45f653c990052b9eb54b6608c7ea302433f464a5b198e), "
             "sections 2-3. Generated by borrowing.py.", "",
             f"Control pairs: {len(controls)} pairs of New Testament letters with no claimed literary relationship.",
             "", "## 1. Whole letters", "",
             "Percentiles are against the control pairs whose shorter letter is between half and twice as long as "
             "this pair's shorter letter.", "",
             "| pair | kind | shorter (words) | comparable controls | rare shared words per 1,000 | percentile | "
             "shared 4-lemma strings per 1,000 | percentile | same order (Spearman) | longest shared string | verdict |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    details = []
    for kind, pairs in [("calibration (known borrowing)", CALIBRATION), ("under test", TESTS),
                        ("reference (gospels)", REFERENCE)]:
        for a, b in pairs:
            result = compare(books, totals, a, b)
            comparable_rare = []
            comparable_strings = []
            for control in controls:
                if result["shorter"] / 2 <= control["shorter"] <= result["shorter"] * 2:
                    comparable_rare.append(control["rare_rate"])
                    comparable_strings.append(control["string_rate"])
            rare_pct = percentile_of(result["rare_rate"], comparable_rare)
            string_pct = percentile_of(result["string_rate"], comparable_strings)
            if not comparable_rare:
                verdict = "no comparable controls"
            elif string_pct > 95 and rare_pct > 90:
                verdict = "borrowing-like"
            elif rare_pct > 90:
                verdict = "shared vocabulary or tradition"
            else:
                verdict = "no sign"
            order = "n/a" if result["order"] is None else f"{result['order']:.2f}"
            lines.append(f"| {result['pair']} | {kind} | {result['shorter']:,} | {len(comparable_rare)} | "
                         f"{result['rare_rate']:.1f} | {rare_pct:.0f} | {result['string_rate']:.1f} | "
                         f"{string_pct:.0f} | {order} | {result['longest']} | {verdict} |")
            details.append(result)
    lines.append("")
    lines.append("### Control pairs: spread")
    lines.append("")
    rare_values = []
    string_values = []
    for control in controls:
        rare_values.append(control["rare_rate"])
        string_values.append(control["string_rate"])
    rare_values.sort()
    string_values.sort()
    lines.append(f"Rare shared words per 1,000: median {rare_values[len(rare_values) // 2]:.1f}, highest "
                 f"{rare_values[-1]:.1f}. Shared strings per 1,000: median {string_values[len(string_values) // 2]:.1f}, "
                 f"highest {string_values[-1]:.1f}.")
    lines.append("")
    top = sorted(controls, key=string_rate_of, reverse=True)[:8]
    lines.append("Control pairs with the most shared strings (to see what non-borrowing overlap looks like):")
    lines.append("")
    for control in top:
        lines.append(f"- {control['pair']}: {control['string_rate']:.1f} per 1,000 ({len(control['strings'])} strings), "
                     f"rare shared words {control['rare_rate']:.1f} per 1,000")
    lines.append("")
    lines.append("### What each pair shares")
    lines.append("")
    for result in details:
        lines.append(f"**{result['pair']}.** Rare shared words ({len(result['rare'])}): {', '.join(sorted(result['rare']))}.")
        lines.append("")
        shown = []
        for gram in result["strings"][:40]:
            shown.append(" ".join(gram))
        more = "" if len(result["strings"]) <= 40 else f" (and {len(result['strings']) - 40} more)"
        lines.append(f"Shared 4-lemma strings ({len(result['strings'])}): {'; '.join(shown)}{more}.")
        lines.append("")
        lines.append(f"Longest shared string ({result['longest']} lemmas): {' '.join(result['longest_words'])}.")
        lines.append("")

    idf = idf_table(books)
    romans13 = passage(books, "Ro", 13, 1, 7)
    lines.append("## 2. Passages: Romans 13:1-7")
    lines.append("")
    for book, size, chapter, first, last, label in [("Mk", 5, 12, 13, 17, "Mark 12:13-17"),
                                                    ("1Pe", 7, 2, 13, 17, "the best window overlapping 1 Peter 2:13-17")]:
        scored = windows(books, book, size, romans13, idf)
        place = None
        for index, item in enumerate(scored):
            overlap = 0
            for verse in range(item[4], item[4] + size):
                if item[3] == chapter and first <= verse <= last:
                    overlap += 1
            if place is None and overlap >= 3 and (book != "Mk" or item[4] == first):
                place = index
        lines.append(f"### Every {size}-verse window of {book} against Romans 13:1-7")
        lines.append("")
        if place is not None:
            lines.append(f"{label} ({scored[place][1]}): rank {place + 1} of {len(scored)} (top {100.0 * (place + 1) / len(scored):.1f}%), "
                         f"score {scored[place][0]:.1f}; shared content words: {', '.join(scored[place][2])}.")
        lines.append("")
        lines.append("| rank | window | score | shared content words |")
        lines.append("|---|---|---|---|")
        for index, item in enumerate(scored[:8]):
            lines.append(f"| {index + 1} | {item[1]} | {item[0]:.1f} | {', '.join(item[2])} |")
        lines.append("")
    lines.append("### Romans 13:1-7 against the three versions of the Caesar saying, and 1 Peter 2:13-17")
    lines.append("")
    lines.append("| passage | score | shared content words | shared strings of 3+ lemmas |")
    lines.append("|---|---|---|---|")
    caesar = [("Mark 12:13-17", passage(books, "Mk", 12, 13, 17)), ("Matthew 22:15-22", passage(books, "Mt", 22, 15, 22)),
              ("Luke 20:20-26", passage(books, "Lk", 20, 20, 26)), ("1 Peter 2:13-17", passage(books, "1Pe", 2, 13, 17))]
    for name, verses in caesar:
        score, shared = similarity(verses, romans13, idf)
        strings = strings_between(verses, romans13, 3)
        lines.append(f"| {name} | {score:.1f} | {', '.join(shared)} | {'; '.join(strings) if strings else 'none'} |")
    lines.append("")
    lines.append("Benchmark (known copying): Mark 12:13-17 against its parallels.")
    lines.append("")
    lines.append("| pair | score | shared strings of 3+ lemmas |")
    lines.append("|---|---|---|")
    mark = caesar[0][1]
    for name, verses in caesar[1:3]:
        score, shared = similarity(mark, verses, idf)
        lines.append(f"| Mark 12:13-17 / {name} | {score:.1f} | {len(strings_between(mark, verses, 3))} |")
    lines.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
