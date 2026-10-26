"""
    rhetoric_across: do language-neutral features of argument survive translation from Greek to Latin, and does a
    known forger of Paul (the Letter to the Laodiceans) copy Paul's words, his way of arguing, or both?
    Rules in rhetoric_across/PREDICTIONS.md (SHA-256 76bf0f0b…a8b).

    Needs sblgnt/ (MorphGNT) and the Clementine Vulgate (python rhetoric_across/fetch_texts.py). Part 2 needs
    rhetoric_across/laodiceans.txt: the 20 verses of Lightfoot's Latin text, one per line (see WRITEUP.md).

    Output: RESULTS.md.

    Usage (from the kit folder):   python -X utf8 rhetoric_across/rhetoric_across.py
"""
import hashlib
import json
import math
import os
import re
import sys
import unicodedata
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
SBLGNT = os.path.join(KIT, "sblgnt")
VULGATE = os.path.join(HERE, "vulgate", "new_testament.json")
LAODICEANS = os.path.join(HERE, "laodiceans.txt")
OUTPUT = os.path.join(HERE, "RESULTS.md")

LETTERS = [("Ro", "Romans"), ("1Co", "1 Corinthians"), ("2Co", "2 Corinthians"), ("Ga", "Galatians"),
           ("Eph", "Ephesians"), ("Php", "Philippians"), ("Col", "Colossians"), ("1Th", "1 Thessalonians"),
           ("2Th", "2 Thessalonians"), ("1Ti", "1 Timothy"), ("2Ti", "2 Timothy"), ("Tit", "Titus"),
           ("Phm", "Philemon"), ("Heb", "Hebrews"), ("Jas", "James"), ("1Pe", "1 Peter"), ("2Pe", "2 Peter"),
           ("1Jn", "1 John"), ("2Jn", "2 John"), ("3Jn", "3 John"), ("Jud", "Jude")]
PAUL = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm"]
FEATURES = ["questions", "sentence length", "by no means", "what then", "not ... but", "conditionals", "for",
            "therefore", "citation formula", "you", "we", "brothers"]
ARGUMENT = ["questions", "by no means", "what then", "not ... but", "conditionals", "for", "therefore",
            "citation formula"]
GREEK = {
    "conditionals": {"ει", "εαν", "ειπερ"},
    "for": {"γαρ"},
    "therefore": {"ουν", "αρα", "διο"},
    "citation formula": {"γεγραπται", "γραφη", "γραφησ", "γραφην", "γραφαι", "γραφαισ", "γραφων"},
    "you": {"συ", "σου", "σοι", "σε", "υμεισ", "υμων", "υμιν", "υμασ"},
    "we": {"ημεισ", "ημων", "ημιν", "ημασ"},
    "brothers": {"αδελφοι"},
}
GREEK_NEGATIONS = {"ου", "ουκ", "ουχ", "μη"}
LATIN = {
    "conditionals": {"si", "nisi"},
    "for": {"enim", "nam"},
    "therefore": {"ergo", "igitur", "itaque", "ideo", "ideoque"},
    "you": {"tu", "te", "tibi", "tui", "uos", "uobis", "uestri", "uestrum"},
    "we": {"nos", "nobis", "nostri", "nostrum"},
    "brothers": {"fratres"},
}
LATIN_NEGATIONS = {"non", "nec", "neque"}


def greek_plain(token):
    token = unicodedata.normalize("NFD", token.lower())
    kept = []
    for character in token:
        if not unicodedata.combining(character):
            kept.append(character)
    return re.sub(r"[^α-ω]", "", "".join(kept).replace("ς", "σ"))


def latin_plain(token):
    return re.sub(r"[^a-z]", "", token.lower().replace("j", "i").replace("v", "u"))


def greek_letter(book):
    """Sentences of one letter: each a list of plain words; the flag says whether it ends with a question mark."""
    paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
    if not paths:
        sys.exit(f"No MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
    sentences = []
    current = []
    with open(paths[0], encoding="utf8") as file:
        for line in file:
            raw = line.split()[3]
            word = greek_plain(raw)
            if word:
                current.append(word)
            end = unicodedata.normalize("NFC", raw)[-1:]
            if end in (";", ";", "."):
                sentences.append((current, end != "."))
                current = []
    if current:
        sentences.append((current, False))
    return sentences


def latin_sentences(text):
    sentences = []
    current = []
    for raw in text.split():
        word = latin_plain(raw)
        if word:
            current.append(word)
        end = raw.rstrip("\"'»)]")[-1:]
        if end in (".", "?", "!"):
            sentences.append((current, end == "?"))
            current = []
    if current:
        sentences.append((current, False))
    return sentences


def latin_letters():
    if not os.path.exists(VULGATE):
        sys.exit(f"Missing {VULGATE}. Run: python rhetoric_across/fetch_texts.py")
    with open(VULGATE, encoding="utf8") as file:
        books = json.load(file)
    texts = {}
    for book in books:
        verses = []
        for chapter in book["chapters"]:
            for verse in chapter["verses"]:
                verses.append(verse["textLatin"])
        texts[book["title"]] = " ".join(verses)
    found = {}
    for code, title in LETTERS:
        if title not in texts:
            sys.exit(f"'{title}' not found in the Vulgate file")
        found[code] = latin_sentences(texts[title])
    return found


def count_phrase(words, first, seconds):
    count = 0
    for index in range(len(words) - 1):
        if words[index] == first and words[index + 1] in seconds:
            count += 1
    return count


def features(sentences, language):
    words = []
    for sentence, question in sentences:
        words.extend(sentence)
    total = len(words)
    table = GREEK if language == "greek" else LATIN
    counts = {}
    for name, forms in table.items():
        count = 0
        for word in words:
            if word in forms:
                count += 1
        counts[name] = count
    if language == "latin":
        count = 0
        for word in words:
            if word.startswith("scriptur") or word == "scriptum":
                count += 1
        counts["citation formula"] = count
    questions = 0
    contrasts = 0
    negations = GREEK_NEGATIONS if language == "greek" else LATIN_NEGATIONS
    adversative = "αλλα" if language == "greek" else "sed"
    for sentence, question in sentences:
        if question:
            questions += 1
        seen_negation = False
        for word in sentence:
            if word in negations:
                seen_negation = True
            if word == adversative and seen_negation:
                contrasts += 1
                break
    counts["questions"] = questions
    counts["not ... but"] = contrasts
    if language == "greek":
        counts["by no means"] = count_phrase(words, "μη", {"γενοιτο"})
        counts["what then"] = count_phrase(words, "τι", {"ουν"})
    else:
        counts["by no means"] = words.count("absit")
        counts["what then"] = count_phrase(words, "quid", {"ergo", "igitur"})
    rates = {}
    for name in FEATURES:
        if name == "sentence length":
            rates[name] = total / max(1, len(sentences))
        else:
            rates[name] = 1000.0 * counts[name] / max(1, total)
    rates["words"] = total
    return rates


def ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    position = 0
    while position < len(order):
        end = position
        while end + 1 < len(order) and values[order[end + 1]] == values[order[position]]:
            end += 1
        for index in range(position, end + 1):
            result[order[index]] = (position + end) / 2.0
        position = end + 1
    return result


def spearman(first, second):
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
        return float("nan")
    return top / math.sqrt(left * right)


def standardise(rows, names):
    result = {}
    for name in names:
        values = []
        for code in rows:
            values.append(rows[code][name])
        mean = sum(values) / len(values)
        squares = 0.0
        for value in values:
            squares += (value - mean) ** 2
        spread = math.sqrt(squares / len(values)) or 1.0
        for code in rows:
            result.setdefault(code, {})[name] = (rows[code][name] - mean) / spread
    return result


def argument_score(rates):
    total = 0.0
    for name in ARGUMENT:
        total += rates[name]
    return total


def trigrams(words):
    found = set()
    for index in range(len(words) - 2):
        found.add(" ".join(words[index:index + 3]))
    return found


def passages(sentences, size):
    """Consecutive, non-overlapping passages of at least `size` words, cut at sentence ends."""
    pieces = []
    current = []
    count = 0
    for sentence in sentences:
        current.append(sentence)
        count += len(sentence[0])
        if count >= size:
            pieces.append(current)
            current = []
            count = 0
    return pieces


def part_two(latin, lines):
    lines.append("## 3. Part 2: the Letter to the Laodiceans")
    lines.append("")
    if not os.path.exists(LAODICEANS):
        lines.append("rhetoric_across/laodiceans.txt not found; Part 2 not run (see WRITEUP.md for how to add it).")
        lines.append("")
        return
    with open(LAODICEANS, "rb") as file:
        digest = hashlib.sha256(file.read()).hexdigest()
    with open(LAODICEANS, encoding="utf8") as file:
        text = file.read()
    text = re.sub(r"(?m)^\s*\d+[.:]?\s*", " ", text)
    sentences = latin_sentences(text)
    words = []
    for sentence, question in sentences:
        words.extend(sentence)
    size = len(words)
    lines.append(f"laodiceans.txt SHA-256 {digest}; {size} words, {len(sentences)} sentences.")
    lines.append("")
    if size < 100:
        lines.append("Fewer than 100 words: check the file. Part 2 not run.")
        lines.append("")
        return
    paul_words = {}
    for code in PAUL:
        flat = []
        for sentence, question in latin[code]:
            flat.extend(sentence)
        paul_words[code] = flat
    all_paul = set()
    for code in PAUL:
        all_paul |= trigrams(paul_words[code])
    own = trigrams(words)
    share = 100.0 * len(own & all_paul) / max(1, len(own))
    baseline = []
    scores = []
    for code in PAUL:
        others = set()
        for other in PAUL:
            if other != code:
                others |= trigrams(paul_words[other])
        for piece in passages(latin[code], size):
            piece_words = []
            for sentence, question in piece:
                piece_words.extend(sentence)
            grams = trigrams(piece_words)
            baseline.append(100.0 * len(grams & others) / max(1, len(grams)))
            scores.append(argument_score(features(piece, "latin")))
    baseline.sort()
    scores.sort()
    rates = features(sentences, "latin")
    score = argument_score(rates)
    below = 0
    for value in scores:
        if value < score:
            below += 1
    percentile = 100.0 * below / len(scores)
    above_all = share > baseline[-1]
    lines.append("### L1. Words: 3-word sequences found in the Latin Paul")
    lines.append("")
    lines.append(f"Laodiceans: {share:.1f}% of its {len(own)} 3-word sequences occur in Paul's 13 letters.")
    lines.append(f"Baseline, {len(baseline)} passages of Paul of the same length against Paul's other letters: "
                 f"median {baseline[len(baseline) // 2]:.1f}%, highest {baseline[-1]:.1f}%.")
    lines.append(f"Pasted from Paul (above every baseline passage): {'yes' if above_all else 'no'}.")
    lines.append("")
    lines.append("### L2. Argument: the argument score against passages of the Latin Paul of the same length")
    lines.append("")
    lines.append(f"Laodiceans: argument score {score:.1f} per 1,000 words. Paul's {len(scores)} passages: 5th "
                 f"percentile {scores[int(0.05 * (len(scores) - 1))]:.1f}, median {scores[len(scores) // 2]:.1f}. "
                 f"Laodiceans is above {percentile:.1f}% of them.")
    lines.append(f"Lacks Paul's argument (below the 5th percentile): {'yes' if percentile < 5 else 'no'}.")
    lines.append("")
    lines.append("| feature | Laodiceans (per 1,000 words) | Latin Paul, whole (per 1,000 words) |")
    lines.append("|---|---|---|")
    whole = []
    for code in PAUL:
        whole.extend(latin[code])
    paul_rates = features(whole, "latin")
    for name in FEATURES:
        lines.append(f"| {name} | {rates[name]:.1f} | {paul_rates[name]:.1f} |")
    lines.append("")
    lines.append("Laodiceans's 3-word sequences found in Paul: " + "; ".join(sorted(own & all_paul)) + ".")
    lines.append("")
    lines.append("### L2b. Exploratory (AMENDMENTS.md 1): Paul's own openings")
    lines.append("")
    lines.append(f"The argument score of the first {size} words of each of Paul's letters (greeting, thanksgiving, "
                 "prayer), the part of a letter Laodiceans most resembles.")
    lines.append("")
    lines.append("| letter | argument score of its opening |")
    lines.append("|---|---|")
    openings_below = 0
    for code in PAUL:
        opening = []
        count = 0
        for sentence in latin[code]:
            if count >= size:
                break
            opening.append(sentence)
            count += len(sentence[0])
        value = argument_score(features(opening, "latin"))
        if value < score:
            openings_below += 1
        lines.append(f"| {code} | {value:.1f} |")
    lines.append("")
    lines.append(f"Laodiceans ({score:.1f}) is above {openings_below} of Paul's 13 openings.")
    lines.append("")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    greek = {}
    for code, title in LETTERS:
        greek[code] = greek_letter(code)
    latin = latin_letters()
    greek_rates = {}
    latin_rates = {}
    for code, title in LETTERS:
        greek_rates[code] = features(greek[code], "greek")
        latin_rates[code] = features(latin[code], "latin")

    lines = ["# rhetoric_across: results", "",
             "Rules: PREDICTIONS.md (SHA-256 76bf0f0b0c0bf9815e37fcfd214f31c7d91bcdd6fecd359e36b284aa5398ea8b). "
             "Generated by rhetoric_across.py.", "",
             "## 1. Part 1, V1: does each feature survive translation?", "",
             "Spearman correlation between the Greek and Latin values across the 21 letters. A feature survives at 0.7 "
             "or more.", "",
             "| feature | correlation | survives |", "|---|---|---|"]
    surviving = []
    for name in FEATURES:
        first = []
        second = []
        for code, title in LETTERS:
            first.append(greek_rates[code][name])
            second.append(latin_rates[code][name])
        rho = spearman(first, second)
        keep = rho >= 0.7
        if keep:
            surviving.append(name)
        lines.append(f"| {name} | {rho:.2f} | {'yes' if keep else 'no'} |")
    lines.append("")
    lines.append(f"Surviving features: {len(surviving)} of {len(FEATURES)}.")
    lines.append("")
    lines.append("## 2. Part 1, V2: does each Latin letter find its own Greek letter?")
    lines.append("")
    matched = 0
    rows = []
    if surviving:
        greek_z = standardise(greek_rates, surviving)
        latin_z = standardise(latin_rates, surviving)
        for code, title in LETTERS:
            best = None
            best_distance = None
            for other, other_title in LETTERS:
                total = 0.0
                for name in surviving:
                    total += (latin_z[code][name] - greek_z[other][name]) ** 2
                distance = math.sqrt(total)
                if best_distance is None or distance < best_distance:
                    best = other
                    best_distance = distance
            if best == code:
                matched += 1
            rows.append(f"| {code} | {best} | {'yes' if best == code else ''} |")
    rate = 100.0 * matched / len(LETTERS)
    lines.append(f"Match rate: {matched} of {len(LETTERS)} ({rate:.0f}%); chance is about 5%. "
                 f"Success (at least 50%): {'yes' if rate >= 50 else 'no'}.")
    lines.append("")
    lines.append("| Latin letter | nearest Greek letter | same |")
    lines.append("|---|---|---|")
    lines.extend(rows)
    lines.append("")
    lines.append("### The values (per 1,000 words; sentence length in words)")
    lines.append("")
    header = "| letter | words (Greek / Latin) |"
    rule = "|---|---|"
    for name in FEATURES:
        header += f" {name} |"
        rule += "---|"
    lines.append(header)
    lines.append(rule)
    for code, title in LETTERS:
        row = f"| {code} | {greek_rates[code]['words']:,} / {latin_rates[code]['words']:,} |"
        for name in FEATURES:
            row += f" {greek_rates[code][name]:.1f} / {latin_rates[code][name]:.1f} |"
        lines.append(row)
    lines.append("")
    part_two(latin, lines)
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
