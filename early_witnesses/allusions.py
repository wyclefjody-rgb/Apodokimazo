"""
    allusions: the 1905 Oxford committee's list of allusions to Paul in the Apostolic Fathers, sorted by Marcion's
    gaps. Rules in early_witnesses/ALLUSIONS_PREDICTIONS.md (SHA-256 166b48c2…f513), with AMENDMENTS.md 3.

    Reads early_witnesses/allusion_codes.txt (hand-coded from the book) and sblgnt/ (for the share of Paul's words
    in each class).

    Output: ALLUSIONS_RESULTS.md.

    Usage (from the kit folder):   python -X utf8 early_witnesses/allusions.py
"""
import os
import sys
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
SBLGNT = os.path.join(KIT, "sblgnt")
CODES = os.path.join(HERE, "allusion_codes.txt")
OUTPUT = os.path.join(HERE, "ALLUSIONS_RESULTS.md")

TEN = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "Phm"]
PASTORALS = ["1Ti", "2Ti", "Tit"]
ABSENT = [("Ro", (8, 12), (10, 1)), ("Ro", (10, 5), (11, 32)), ("Ga", (3, 6), (3, 9)), ("Ga", (3, 15), (3, 16)),
          ("Eph", (6, 2), (6, 3)), ("Col", (1, 16), (1, 16))]
PROBABLY_ABSENT = [("Ro", (15, 1), (16, 27))]
WITNESSES = ["1 Clement", "Ignatius", "Polycarp"]
OTHERS = ["Barnabas", "Didache", "Hermas", "2 Clement"]
GRADES = ["a", "b", "c", "d", "u"]
CLASSES = ["A", "B", "C", "D"]


def inside(book, place, spans):
    for span_book, first, last in spans:
        if span_book == book and first <= place <= last:
            return True
    return False


def class_of_verse(book, place):
    if book in PASTORALS:
        return "D"
    if inside(book, place, ABSENT):
        return "B"
    if inside(book, place, PROBABLY_ABSENT):
        return "C"
    return "A"


def parse_reference(text):
    """'Ro 9:7-13' -> ('Ro', 9, 7, 13, changed). A trailing * marks a changed phrase."""
    changed = text.endswith("*")
    if changed:
        text = text[:-1]
    book, place = text.split()
    chapter, verses = place.split(":")
    if "-" in verses:
        first, last = verses.split("-")
    else:
        first = verses
        last = verses
    return book, int(chapter), int(first), int(last), changed


def class_of_reference(text):
    book, chapter, first, last, changed = parse_reference(text)
    if book not in TEN and book not in PASTORALS:
        sys.exit(f"Not a letter of Paul: {text}")
    if changed:
        return "B"
    found = []
    for verse in range(first, last + 1):
        found.append(class_of_verse(book, (chapter, verse)))
    for label in ["B", "C", "D"]:
        if label in found:
            return label
    return "A"


def read_codes():
    entries = []
    with open(CODES, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = []
            for part in line.split("|"):
                fields.append(part.strip())
            while len(fields) < 7:
                fields.append("")
            writer, number, passage, references, grade, page, note = fields[:7]
            classes = []
            if references != "-":
                for reference in references.split(";"):
                    label = class_of_reference(reference.strip())
                    if label not in classes:
                        classes.append(label)
            entries.append({"writer": writer, "number": number, "passage": passage, "references": references,
                            "grade": grade, "page": page, "note": note, "classes": classes})
    return entries


def class_shares():
    counts = {"A": 0, "B": 0, "C": 0}
    books = {}
    for book in TEN:
        books[book] = {"A": 0, "B": 0, "C": 0}
        paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
        if not paths:
            sys.exit(f"Missing the MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
        with open(paths[0], encoding="utf8") as file:
            for line in file:
                columns = line.split()
                place = (int(columns[0][2:4]), int(columns[0][4:6]))
                label = class_of_verse(book, place)
                counts[label] += 1
                books[book][label] += 1
    return counts, books


def entry_chance(entry, books):
    """Share of class-B words in the letters this entry cites (an entry citing Romans and Galatians uses both)."""
    cited = []
    for reference in entry["references"].split(";"):
        book = reference.strip().split()[0]
        if book in TEN and book not in cited:
            cited.append(book)
    words = 0
    absent = 0
    for book in cited:
        words += books[book]["A"] + books[book]["B"] + books[book]["C"]
        absent += books[book]["B"]
    if words == 0:
        return 0.0
    return absent / words


def at_most_varied(count, chances):
    """Chance of at most count successes when each trial has its own chance (Poisson binomial)."""
    table = [1.0]
    for chance in chances:
        grown = [0.0] * (len(table) + 1)
        for index in range(len(table)):
            grown[index] += table[index] * (1 - chance)
            grown[index + 1] += table[index] * chance
        table = grown
    total = 0.0
    for index in range(min(count, len(table) - 1) + 1):
        total += table[index]
    return total


def counted(entries, writer, grades):
    chosen = []
    for entry in entries:
        if entry["writer"] == writer and entry["grade"] in grades and entry["classes"]:
            chosen.append(entry)
    return chosen


def with_class(entries, labels):
    chosen = []
    for entry in entries:
        for label in labels:
            if label in entry["classes"]:
                chosen.append(entry)
                break
    return chosen


def ten_letter_entries(entries):
    return with_class(entries, ["A", "B", "C"])


def binomial_at_most(count, trials, chance):
    total = 0.0
    for value in range(count + 1):
        ways = 1.0
        for step in range(value):
            ways = ways * (trials - step) / (step + 1)
        total += ways * chance ** value * (1 - chance) ** (trials - value)
    return total


def label_of(entry):
    return f"{entry['writer']} ({entry['number']}) {entry['passage']} ~ {entry['references']}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    entries = read_codes()
    counts, books = class_shares()
    total = counts["A"] + counts["B"] + counts["C"]
    share_b = counts["B"] / total
    share_c = counts["C"] / total
    out = []
    out.append("# The 1905 allusion list against Marcion's gaps: results")
    out.append("")
    out.append("Rules: ALLUSIONS_PREDICTIONS.md (SHA-256 166b48c2…f513) and AMENDMENTS.md 3. Codes: allusion_codes.txt,")
    out.append("from *The New Testament in the Apostolic Fathers* (Oxford, 1905). Coding by Claude (an AI model), for review.")
    out.append("")
    out.append("## 1. How much of Paul is in each class")
    out.append("")
    out.append("Words of the ten letters of Marcion's collection (SBLGNT):")
    out.append("")
    out.append("| class | words | share |")
    out.append("|---|---|---|")
    for label in ["A", "B", "C"]:
        out.append(f"| {label} | {counts[label]:,} | {100 * counts[label] / total:.1f}% |")
    out.append("")
    out.append("## 2. Entries by writer, grade and class")
    out.append("")
    out.append("An entry that cites passages of two classes is counted under both. u = unclassed.")
    out.append("")
    out.append("| writer | class | a | b | c | d | u |")
    out.append("|---|---|---|---|---|---|---|")
    for writer in WITNESSES + OTHERS:
        for label in CLASSES:
            cells = []
            for grade in GRADES:
                cells.append(str(len(with_class(counted(entries, writer, [grade]), [label]))))
            out.append(f"| {writer} | {label} | " + " | ".join(cells) + " |")
    out.append("")
    out.append("## 3. Every entry outside class A")
    out.append("")
    for label in ["B", "C", "D"]:
        out.append(f"**Class {label}**")
        out.append("")
        for writer in WITNESSES + OTHERS:
            for entry in with_class(counted(entries, writer, GRADES), [label]):
                note = ""
                if entry["note"]:
                    note = f" ({entry['note']})"
                out.append(f"- {label_of(entry)}: grade {entry['grade']}, p. {entry['page']}{note}")
        out.append("")
    out.append("## 4. Predictions")
    out.append("")
    clement = with_class(counted(entries, "1 Clement", ["a", "b", "c"]), ["B", "C"])
    polycarp = with_class(counted(entries, "Polycarp", ["a", "b", "c"]), ["D"])
    three = []
    for writer in WITNESSES:
        for entry in with_class(counted(entries, writer, ["a", "b", "c"]), ["B", "C"]):
            three.append(entry)
    strong = []
    for entry in three:
        if entry["grade"] in ["a", "b"]:
            strong.append(entry)
    rows = []
    rows.append(("1. 1 Clement: an a-c allusion to class B or C", len(clement) >= 1, f"{len(clement)} found"))
    rows.append(("2. Polycarp: an a-c allusion to class D", len(polycarp) >= 1, f"{len(polycarp)} found"))
    rows.append(("3. At least 3 a-c allusions to class B or C across the three", len(three) >= 3, f"{len(three)} found"))
    floor = share_b / 3
    fours = []
    lines = []
    for grades, name in [(["a", "b", "c", "d"], "graded a-d"), (["a", "b", "c"], "graded a-c")]:
        for writer in WITNESSES:
            pool = ten_letter_entries(counted(entries, writer, grades))
            hits = with_class(pool, ["B"])
            share = 0.0
            if pool:
                share = len(hits) / len(pool)
            expected = len(pool) * share_b
            chance = binomial_at_most(len(hits), len(pool), share_b)
            if grades == ["a", "b", "c", "d"]:
                fours.append(share >= floor)
            lines.append(f"| {writer} | {name} | {len(pool)} | {len(hits)} | {100 * share:.1f}% | {expected:.1f} | "
                         f"{chance:.2f} |")
    rows.append((f"4. Each writer's class-B share at least {100 * floor:.1f}% (a third of {100 * share_b:.1f}%)",
                 all(fours), "see the table below"))
    out.append("| prediction | met? | detail |")
    out.append("|---|---|---|")
    for text, met, detail in rows:
        word = "not met"
        if met:
            word = "met"
        out.append(f"| {text} | {word} | {detail} |")
    out.append("")
    out.append("Prediction 4, per writer. The pool is the writer's entries citing the ten letters (AMENDMENTS.md 3).")
    out.append("\"Expected\" is the pool times class B's share of the words. The last column (exploratory) is the")
    out.append("chance of seeing this few class-B entries or fewer if allusions fell on Paul's words at random.")
    out.append("")
    out.append("| writer | grades | entries citing the ten letters | to class B | share | expected | chance of this few |")
    out.append("|---|---|---|---|---|---|---|")
    for line in lines:
        out.append(line)
    out.append("")
    out.append("Exploratory (AMENDMENTS.md 3): the same, but each entry's chance of landing in class B is class B's")
    out.append("share of the letters that entry cites. This allows for which letters a writer uses: almost all of")
    out.append("class B is in Romans, so a writer who rarely uses Romans is expected to have few class-B entries.")
    out.append("")
    out.append("| writer | grades | entries citing the ten letters | to class B | expected | chance of this few |")
    out.append("|---|---|---|---|---|---|")
    for grades, name in [(["a", "b", "c", "d"], "graded a-d"), (["a", "b", "c"], "graded a-c")]:
        for writer in WITNESSES + OTHERS:
            pool = ten_letter_entries(counted(entries, writer, grades))
            if not pool:
                continue
            hits = with_class(pool, ["B"])
            chances = []
            expected = 0.0
            for entry in pool:
                chance = entry_chance(entry, books)
                chances.append(chance)
                expected += chance
            probability = at_most_varied(len(hits), chances)
            out.append(f"| {writer} | {name} | {len(pool)} | {len(hits)} | {expected:.1f} | {probability:.2f} |")
    out.append("")
    out.append("## 5. Decision rule (section 4 of the predictions)")
    out.append("")
    if strong:
        out.append("At least one a- or b-graded allusion points to class B or C: good evidence of a fuller Paul.")
        for entry in strong:
            out.append(f"- {label_of(entry)}, grade {entry['grade']}")
    elif three:
        out.append("No a- or b-graded allusion points to class B or C. Grade c only, which the rule counts as a hint:")
        for entry in three:
            out.append(f"- {label_of(entry)}, grade {entry['grade']}, p. {entry['page']}")
    else:
        out.append("No a- to c-graded allusion points to class B or C: a point for Livesey's model.")
    out.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"Written: {OUTPUT}")


if __name__ == "__main__":
    main()
