"""
    letter_form: where do Paul's letters fall among ancient letters, in length and in the standard formulas?
    Rules in letter_form/PREDICTIONS.md (SHA-256 aa80ce88…250f).

    Reads, all from the kit:
      letter_period/papyri_letters_accented.json   papyrus letters dated within 1-200 CE (letter_period study)
      sblgnt/                                      Paul and the other New Testament letters
      First1KGreek/                                Ignatius, 1 Clement, Polycarp, the Greek fictional collections
      canonical-greekLit/                          the Greek literary letters, Aelian, Philostratus
      canonical-latinLit/                          Cicero, Seneca, Pliny
    Run letter_form/fetch_texts.py first if any of these is missing.

    Output: RESULTS.md and letters.csv (one row per letter).

    Usage (from the kit folder):   python -X utf8 letter_form/letter_form.py
"""
import csv
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(KIT, "advanced"))
import extract

SBLGNT = os.path.join(KIT, "sblgnt")
PAPYRI = os.path.join(KIT, "letter_period", "papyri_letters_accented.json")
FIRST1K = os.path.join(KIT, "First1KGreek", "data")
PERSEUS = os.path.join(KIT, "canonical-greekLit", "data")
LATIN = os.path.join(KIT, "canonical-latinLit", "data")
RESULTS = os.path.join(HERE, "RESULTS.md")
TABLE = os.path.join(HERE, "letters.csv")
TEI = "{http://www.tei-c.org/ns/1.0}"
DROP = {"note", "bibl", "app", "rdg", "del", "ref", "sic"}

PAUL = [("Ro", "core four"), ("1Co", "core four"), ("2Co", "core four"), ("Ga", "core four"),
        ("Php", "Paul, other undisputed"), ("1Th", "Paul, other undisputed"), ("Phm", "Paul, other undisputed"),
        ("Eph", "Paul, disputed"), ("Col", "Paul, disputed"), ("2Th", "Paul, disputed"),
        ("1Ti", "Pastorals"), ("2Ti", "Pastorals"), ("Tit", "Pastorals")]
OTHER_NT = ["Heb", "Jas", "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jud"]
PAUL_GROUPS = ["core four", "Paul, other undisputed", "Paul, disputed", "Pastorals"]

GREEK_TEI = [
    ("Ignatius", "Ignatius (genuine)", "First1KGreek", "tlg1443", "tlg001", "epistle", ["1", "2", "3", "4", "5", "6", "7"]),
    ("Spurious Ignatius", "spurious Ignatius", "First1KGreek", "tlg1443", "tlg002", "epistle", ["13", "1", "4", "5", "9", "10"]),
    ("1 Clement", "1 Clement and Polycarp", "First1KGreek", "tlg1271", "tlg001", None, None),
    ("Polycarp", "1 Clement and Polycarp", "First1KGreek", "tlg1622", "tlg001", None, None),
    ("Dionysius to Ammaeus", "Greek literary letters", "canonical-greekLit", "tlg0081", "tlg008", None, None),
    ("Dionysius to Pompeius", "Greek literary letters", "canonical-greekLit", "tlg0081", "tlg015", None, None),
    ("Plutarch to his wife", "Greek literary letters", "canonical-greekLit", "tlg0007", "tlg111", None, None),
    ("Arrian, Periplus", "Greek literary letters", "canonical-greekLit", "tlg0074", "tlg004", None, None),
    ("Anacharsis", "Greek fictional letters", "First1KGreek", "tlg0037", "tlg001", "epistle", None),
    ("Chion", "Greek fictional letters", "First1KGreek", "tlg0041", "tlg001", "epistle", None),
    ("Phalaris", "Greek fictional letters", "First1KGreek", "tlg0053", "tlg001", "epistle", None),
    ("Themistocles", "Greek fictional letters", "First1KGreek", "tlg0055", "tlg001", "epistle", None),
    ("Crates", "Greek fictional letters", "First1KGreek", "tlg0623", "tlg001", "epistle", None),
    ("Socrates", "Greek fictional letters", "First1KGreek", "tlg0636", "tlg001", "epistle", None),
    ("Socratics", "Greek fictional letters", "First1KGreek", "tlg0637", "tlg001", "epistle", None),
    ("Diogenes", "Greek fictional letters", "First1KGreek", "tlg1325", "tlg001", "epistle", None),
    ("Euripides", "Greek fictional letters", "First1KGreek", "tlg1367", "tlg001", "epistle", None),
    ("Brutus", "Greek fictional letters", "First1KGreek", "tlg1803", "tlg001", "epistle", None),
    ("Alciphron", "Greek fictional letters", "First1KGreek", "tlg0640", "tlg001", "section", None),
    ("Aelian", "Greek fictional letters", "canonical-greekLit", "tlg0545", "tlg003", "letter", None),
    ("Philostratus", "Greek fictional letters", "canonical-greekLit", "tlg0638", "tlg006", "chapter", None),
]
LATIN_TEI = [
    ("Cicero, to his friends", "Latin: Cicero (real correspondence)", "phi0474", "phi056", None),
    ("Cicero, to Atticus", "Latin: Cicero (real correspondence)", "phi0474", "phi057", None),
    ("Seneca, moral letters", "Latin: Seneca (literary collection)", "phi1017", "phi015", None),
    ("Pliny, books 1-9", "Latin: Pliny 1-9 (literary collection)", "phi1318", "phi001", "1-9"),
    ("Pliny, book 10", "Latin: Pliny 10 (official)", "phi1318", "phi001", "10"),
]
GREEK_GROUPS = ["papyri", "core four", "Paul, other undisputed", "Paul, disputed", "Pastorals", "Paul (all thirteen)",
                "other New Testament letters", "Ignatius (genuine)", "spurious Ignatius", "1 Clement and Polycarp",
                "Greek literary letters", "Greek fictional letters"]
LATIN_GROUPS = ["Latin: Cicero (real correspondence)", "Latin: Seneca (literary collection)",
                "Latin: Pliny 1-9 (literary collection)", "Latin: Pliny 10 (official)"]
PROFILE_FORMULAS = ["everyday greeting", "grace and peace", "everyday farewell", "grace benediction",
                    "greetings passed on"]
FORMULAS = ["everyday greeting", "grace and peace", "thanksgiving", "everyday farewell", "grace benediction",
            "greetings passed on"]
GREEK_FAREWELLS = {"ερρωσο", "ερρωσθε", "ερρωσθαι", "υγιαινε", "ευτυχει", "ευτυχειτε"}
LATIN_SALUTES = {"salutem", "sal", "s", "salute"}
LATIN_FAREWELLS = {"vale", "valete", "uale", "ualete"}


def local(tag):
    return tag.split("}")[-1]


def collect(element, out):
    """Text of an element, keeping headings and the salutation of an opener, dropping notes and apparatus."""
    tag = local(element.tag)
    if tag == "label":
        if element.get("rend") == "opener":
            for inner in element.iter():
                if inner.get("rend") == "salute":
                    out.append(" " + " ".join(inner.itertext()) + " ")
        return
    if tag in DROP:
        return
    if element.text:
        out.append(element.text)
    for child in element:
        collect(child, out)
        if child.tail:
            out.append(child.tail)


def greek_words(element):
    out = []
    collect(element, out)
    words = []
    for token in re.findall(r"\S+", " ".join(out)):
        word = extract.norm(token)
        if word:
            words.append(word)
    return words


def latin_words(element):
    out = []
    collect(element, out)
    words = []
    for token in re.findall(r"\S+", " ".join(out)):
        word = re.sub(r"[^a-z]", "", token.lower())
        if word:
            words.append(word)
    return words


def tei_path(source, author, work):
    folder = {"First1KGreek": FIRST1K, "canonical-greekLit": PERSEUS, "canonical-latinLit": LATIN}[source]
    paths = sorted(glob(os.path.join(folder, author, work, f"{author}.{work}.*grc*.xml")))
    if source == "canonical-latinLit":
        paths = sorted(glob(os.path.join(folder, author, work, f"{author}.{work}.*lat*.xml")))
    if not paths:
        sys.exit(f"Missing {source} {author}.{work}. Run: python letter_form/fetch_texts.py")
    return paths[0]


def divisions(element, level, book, found):
    """Every div of the given subtype, with the number of the book it sits in."""
    for child in element:
        if local(child.tag) != "div":
            continue
        if child.get("subtype") == "book":
            divisions(child, level, child.get("n"), found)
        elif child.get("subtype") == level:
            found.append((book, child.get("n"), child))
        else:
            divisions(child, level, book, found)


def tei_letters(path, level, keep, books, language):
    body = ET.parse(path).getroot().find(f".//{TEI}body")
    reader = greek_words if language == "greek" else latin_words
    if level is None:
        return [("whole", reader(body))]
    found = []
    divisions(body, level, None, found)
    letters = []
    for book, number, div in found:
        if keep is not None and number not in keep:
            continue
        if books == "1-9" and book == "10":
            continue
        if books == "10" and book != "10":
            continue
        label = number if book is None else f"{book}.{number}"
        letters.append((label, reader(div)))
    return letters


def nt_words(book):
    paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
    if not paths:
        sys.exit(f"No MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
    words = []
    with open(paths[0], encoding="utf8") as file:
        for line in file:
            word = extract.norm(line.split()[4])
            if word:
                words.append(word)
    return words


def greek_formulas(words):
    count = len(words)
    first30 = words[:30]
    first60 = words[:60]
    last30 = words[-30:]
    last40 = words[-40:]
    start = max(40, count // 4)
    found = {}
    found["everyday greeting"] = "χαιρειν" in first30
    found["grace and peace"] = "χαρισ" in first60 and "ειρηνη" in first60
    thanks = False
    for word in words[:start]:
        if word.startswith("ευχαριστ") or word == "ευλογητοσ":
            thanks = True
    found["thanksgiving"] = thanks
    farewell = False
    for word in last30:
        if word in GREEK_FAREWELLS:
            farewell = True
    found["everyday farewell"] = farewell
    found["grace benediction"] = "χαρισ" in last40
    greets = False
    for word in words[int(count * 0.7):]:
        if word.startswith("ασπαζ") or word.startswith("ασπασ"):
            greets = True
    found["greetings passed on"] = greets
    return found


def latin_formulas(words):
    count = len(words)
    found = {}
    salute = False
    for word in words[:12]:
        if word in LATIN_SALUTES:
            salute = True
    found["everyday greeting"] = salute
    found["grace and peace"] = False
    found["thanksgiving"] = "gratias" in words[:max(12, count // 4)]
    farewell = False
    for word in words[-15:]:
        if word in LATIN_FAREWELLS:
            farewell = True
    found["everyday farewell"] = farewell
    found["grace benediction"] = False
    greets = False
    for word in words[int(count * 0.7):]:
        if word.startswith("salut"):
            greets = True
    found["greetings passed on"] = greets
    return found


def percentile(values, share):
    ordered = sorted(values)
    if not ordered:
        return float("nan")
    position = share * (len(ordered) - 1)
    low = int(math.floor(position))
    high = int(math.ceil(position))
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def rank_in(value, values):
    below = 0
    for other in values:
        if other < value:
            below += 1
    return 100.0 * below / len(values)


def load_all():
    rows = []
    with open(PAPYRI, encoding="utf8") as file:
        papyri = json.load(file)
    for letter in papyri:
        words = []
        for token in letter["words"]:
            word = extract.norm(token)
            if word:
                words.append(word)
        if words:
            rows.append({"group": "papyri", "text": "papyrus", "letter": letter["hybrid"], "words": words,
                         "language": "greek"})
    for book, group in PAUL:
        rows.append({"group": group, "text": book, "letter": book, "words": nt_words(book), "language": "greek"})
    for book in OTHER_NT:
        rows.append({"group": "other New Testament letters", "text": book, "letter": book, "words": nt_words(book),
                     "language": "greek"})
    for name, group, source, author, work, level, keep in GREEK_TEI:
        for label, words in tei_letters(tei_path(source, author, work), level, keep, None, "greek"):
            if words:
                rows.append({"group": group, "text": name, "letter": label, "words": words, "language": "greek"})
    for name, group, author, work, books in LATIN_TEI:
        path = tei_path("canonical-latinLit", author, work)
        for label, words in tei_letters(path, "letter", None, books, "latin"):
            if words:
                rows.append({"group": group, "text": name, "letter": label, "words": words, "language": "latin"})
    for row in rows:
        if row["language"] == "greek":
            row["formulas"] = greek_formulas(row["words"])
        else:
            row["formulas"] = latin_formulas(row["words"])
        row["length"] = len(row["words"])
    return rows


def members(rows, group):
    chosen = []
    for row in rows:
        if row["group"] == group:
            chosen.append(row)
        elif group == "Paul (all thirteen)" and row["group"] in PAUL_GROUPS:
            chosen.append(row)
    return chosen


def profile(chosen):
    lengths = []
    for row in chosen:
        lengths.append(row["length"])
    values = [math.log10(percentile(lengths, 0.5))]
    for name in PROFILE_FORMULAS:
        count = 0
        for row in chosen:
            if row["formulas"][name]:
                count += 1
        values.append(count / len(chosen))
    return values


def distance(first, second):
    total = 0.0
    for index in range(len(first)):
        total += (first[index] - second[index]) ** 2
    return math.sqrt(total)


def share(chosen, name):
    count = 0
    for row in chosen:
        if row["formulas"][name]:
            count += 1
    return count, len(chosen)


def exploratory(rows, profiles, papyri):
    """Checks added after the first run (AMENDMENTS.md 1). Not part of the decision rules."""
    lines = ["## 6. Exploratory checks (AMENDMENTS.md 1; not part of the decision rules)", "",
             "### 6a. Papyri flagged with a grace formula", "",
             "The last words of each papyrus letter counted as having a grace greeting or benediction:", ""]
    for row in papyri:
        if row["formulas"]["grace and peace"] or row["formulas"]["grace benediction"]:
            lines.append(f"- {row['letter']}: ... {' '.join(row['words'][-40:])}")
    lines.append("")
    lines.append("### 6b. Long opening greetings: the same greetings searched in the first 150 words")
    lines.append("")
    lines.append("| group | letters | everyday greeting (first 150) | grace and peace (first 150) |")
    lines.append("|---|---|---|---|")
    for group in GREEK_GROUPS:
        chosen = members(rows, group)
        greeting = 0
        grace = 0
        for row in chosen:
            opening = row["words"][:150]
            if "χαιρειν" in opening:
                greeting += 1
            if "χαρισ" in opening and "ειρηνη" in opening:
                grace += 1
        lines.append(f"| {group} | {len(chosen)} | {100.0 * greeting / len(chosen):.0f}% | "
                     f"{100.0 * grace / len(chosen):.0f}% |")
    lines.append("")
    lines.append("### 6c. What drives the distances")
    lines.append("")
    lines.append("Distances recomputed from parts of the profile: length only; the everyday frame only (everyday "
                 "greeting and farewell); the Christian formulas only (grace and peace, grace benediction, greetings "
                 "passed on).")
    lines.append("")
    parts = [("length only", [0]), ("everyday frame only", [1, 3]), ("Christian formulas only", [2, 4, 5])]
    header = "| group |"
    rule = "|---|"
    for name, indexes in parts:
        header += f" {name}: to papyri | to Paul |"
        rule += "---|---|"
    lines.append(header)
    lines.append(rule)
    for group in ["Greek fictional letters", "Greek literary letters", "Ignatius (genuine)", "spurious Ignatius",
                  "Pastorals", "core four"]:
        row = f"| {group} |"
        for name, indexes in parts:
            first = []
            papyri_part = []
            paul_part = []
            for index in indexes:
                first.append(profiles[group][index])
                papyri_part.append(profiles["papyri"][index])
                paul_part.append(profiles["Paul (all thirteen)"][index])
            row += f" {distance(first, papyri_part):.2f} | {distance(first, paul_part):.2f} |"
        lines.append(row)
    lines.append("")
    return lines


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = load_all()
    papyri = members(rows, "papyri")
    complete = []
    for row in papyri:
        if row["formulas"]["everyday greeting"] and row["formulas"]["everyday farewell"]:
            complete.append(row["length"])
    all_lengths = []
    for row in papyri:
        all_lengths.append(row["length"])

    lines = ["# letter_form: results", "",
             "Rules: PREDICTIONS.md (SHA-256 aa80ce8823a32e647108a525437de1324845116df35850dab2113a226fb6250f). "
             "Generated by letter_form.py.", "",
             "## 1. Papyrus letter lengths (1-200 CE)", "",
             "| papyri | letters | median | 90th percentile | 95th | 99th | longest |", "|---|---|---|---|---|---|---|"]
    for name, values in [("all", all_lengths), ("complete (greeting and farewell both present)", complete)]:
        lines.append(f"| {name} | {len(values)} | {percentile(values, 0.5):.0f} | {percentile(values, 0.9):.0f} | "
                     f"{percentile(values, 0.95):.0f} | {percentile(values, 0.99):.0f} | {max(values)} |")
    lines.append("")
    lines.append("## 2. Paul's letters against the papyri")
    lines.append("")
    lines.append("| letter | group | words | longer than this % of complete papyri | " + " | ".join(FORMULAS) + " |")
    lines.append("|---|---|---|---|" + "---|" * len(FORMULAS))
    p95 = percentile(complete, 0.95)
    above = 0
    for book, group in PAUL:
        for row in rows:
            if row["text"] == book and row["group"] == group:
                marks = []
                for name in FORMULAS:
                    marks.append("yes" if row["formulas"][name] else "")
                if row["length"] > p95:
                    above += 1
                lines.append(f"| {book} | {group} | {row['length']:,} | {rank_in(row['length'], complete):.1f} | "
                             + " | ".join(marks) + " |")
    lines.append("")
    lines.append(f"Paul's letters longer than the 95th percentile of complete papyri ({p95:.0f} words): {above} of 13.")
    lines.append("")
    lines.append("## 3. Every group")
    lines.append("")
    lines.append("Formula columns: share of the group's letters with the formula (Latin equivalents for Latin groups; "
                 "Latin has no grace formulas).")
    lines.append("")
    lines.append("| group | letters | median words | middle half | " + " | ".join(FORMULAS) + " |")
    lines.append("|---|---|---|---|" + "---|" * len(FORMULAS))
    for group in GREEK_GROUPS + LATIN_GROUPS:
        chosen = members(rows, group)
        if not chosen:
            continue
        lengths = []
        for row in chosen:
            lengths.append(row["length"])
        cells = []
        for name in FORMULAS:
            count, total = share(chosen, name)
            cells.append(f"{100.0 * count / total:.0f}%")
        lines.append(f"| {group} | {len(chosen)} | {percentile(lengths, 0.5):,.0f} | {percentile(lengths, 0.25):,.0f}"
                     f" to {percentile(lengths, 0.75):,.0f} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("### Greek fictional and Christian collections one by one")
    lines.append("")
    lines.append("| text | letters | median words | " + " | ".join(FORMULAS) + " |")
    lines.append("|---|---|---|" + "---|" * len(FORMULAS))
    names = []
    for name, group, source, author, work, level, keep in GREEK_TEI:
        names.append(name)
    for name, group, author, work, books in LATIN_TEI:
        names.append(name)
    for name in names:
        chosen = []
        for row in rows:
            if row["text"] == name:
                chosen.append(row)
        lengths = []
        for row in chosen:
            lengths.append(row["length"])
        cells = []
        for formula in FORMULAS:
            count, total = share(chosen, formula)
            cells.append(f"{count}/{total}")
        lines.append(f"| {name} | {len(chosen)} | {percentile(lengths, 0.5):,.0f} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## 4. Profile distances (Greek groups)")
    lines.append("")
    lines.append("Profile: log10 of median length and the shares of five formulas (everyday greeting, grace and "
                 "peace, everyday farewell, grace benediction, greetings passed on). Euclidean distance.")
    lines.append("")
    profiles = {}
    for group in GREEK_GROUPS:
        profiles[group] = profile(members(rows, group))
    lines.append("| group | to papyri | to Paul (all thirteen) | to core four | closer to |")
    lines.append("|---|---|---|---|---|")
    for group in GREEK_GROUPS:
        to_papyri = distance(profiles[group], profiles["papyri"])
        to_paul = distance(profiles[group], profiles["Paul (all thirteen)"])
        to_core = distance(profiles[group], profiles["core four"])
        nearer = "papyri" if to_papyri < to_paul else "Paul"
        lines.append(f"| {group} | {to_papyri:.2f} | {to_paul:.2f} | {to_core:.2f} | {nearer} |")
    lines.append("")
    lines.append("## 5. Decision rules (PREDICTIONS.md section 4)")
    lines.append("")
    grace_count = 0
    for row in papyri:
        if row["formulas"]["grace and peace"] or row["formulas"]["grace benediction"]:
            grace_count += 1
    grace_share = 100.0 * grace_count / len(papyri)
    misfit = above == 13 and grace_share < 2.0
    lines.append(f"- Question 1. Paul's letters above the 95th percentile of complete papyri: {above} of 13; papyri "
                 f"with a grace greeting or grace benediction: {grace_count} of {len(papyri)} ({grace_share:.1f}%). "
                 f"The misfit is real: {'yes' if misfit else 'no'}.")
    fiction = profiles["Greek fictional letters"]
    to_paul = distance(fiction, profiles["Paul (all thirteen)"])
    to_papyri = distance(fiction, profiles["papyri"])
    lines.append(f"- Question 2. Greek fictional letters: distance to Paul {to_paul:.2f}, to the papyri {to_papyri:.2f}. "
                 f"{'Closer to Paul: the misfit fits invented letters.' if to_paul < to_papyri else 'Closer to the papyri: invented letters keep the everyday frame; the misfit is not a sign of fiction.'}")
    for group in ["Pastorals", "spurious Ignatius"]:
        to_core = distance(profiles[group], profiles["core four"])
        to_pap = distance(profiles[group], profiles["papyri"])
        lines.append(f"- {group}: distance to the core four {to_core:.2f}, to the papyri {to_pap:.2f}: closer to "
                     f"{'the core four' if to_core < to_pap else 'the papyri'}.")
    lines.append("")
    lines.extend(exploratory(rows, profiles, papyri))
    with open(RESULTS, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    with open(TABLE, "w", encoding="utf8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["group", "text", "letter", "words"] + FORMULAS + ["first words"])
        for row in rows:
            marks = []
            for name in FORMULAS:
                marks.append(1 if row["formulas"][name] else 0)
            writer.writerow([row["group"], row["text"], row["letter"], row["length"]] + marks
                            + [" ".join(row["words"][:12])])
    print("\n".join(lines))
    print(f"\nWrote {RESULTS}\nWrote {TABLE}")


if __name__ == "__main__":
    main()
