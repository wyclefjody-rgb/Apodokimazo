"""
    rival_witnesses: did groups outside Marcion's circle use Paul by about 160, and did their Paul include what
    Marcion's edition lacked? Rules in rival_witnesses/PREDICTIONS.md (SHA-256 176087ea…13b7db).

    Step 1 (always): finds every 4-word sequence that a Greek witness shares with Paul's 13 letters and that is not
    in the LXX, and every mention of Paul or "the apostle". Writes CANDIDATES.md for hand-coding.
    Step 2 (when codes.txt exists): tallies the hand-coded uses against the predictions. Writes RESULTS.md.

    Needs sblgnt/, lxx/ (setup_data.py), and the witness texts (python rival_witnesses/fetch_texts.py).

    Usage (from the kit folder):   python -X utf8 rival_witnesses/rival_witnesses.py
"""
import csv
import os
import sys
import xml.etree.ElementTree as ET
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(KIT, "advanced"))
import extract

SBLGNT = os.path.join(KIT, "sblgnt")
LXX = os.path.join(KIT, "lxx", "01_wordlist_unicode", "text_accented.csv")
WITNESSES = os.path.join(HERE, "witnesses.txt")
CODES = os.path.join(HERE, "codes.txt")
CANDIDATES = os.path.join(HERE, "CANDIDATES.md")
RESULTS = os.path.join(HERE, "RESULTS.md")
NS = "{http://www.tei-c.org/ns/1.0}"
SIZE = 4
CONTEXT = 12

PAUL = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm"]
TEN = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "Phm"]
PASTORALS = ["1Ti", "2Ti", "Tit"]
ABSENT = [("Ro", (8, 12), (10, 1)), ("Ro", (10, 5), (11, 32)), ("Ga", (3, 6), (3, 9)), ("Ga", (3, 15), (3, 16)),
          ("Eph", (6, 2), (6, 3)), ("Col", (1, 16), (1, 16))]
PROBABLY_ABSENT = [("Ro", (15, 1), (16, 27))]
TIER_ONE = ["Valentinus", "Basilides and Isidore", "Ptolemy", "Justin", "Epistle of the Apostles"]
GRADES = ["Q", "V", "A", "D"]


def read_lines(path):
    rows = []
    with open(path, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = []
            for part in line.split("|"):
                fields.append(part.strip())
            rows.append(fields)
    return rows


def normalised(text):
    words = []
    for word in text.split():
        cleaned = extract.norm(word)
        if cleaned:
            words.append(cleaned)
    return words


def is_textpart(element):
    return element.tag == NS + "div" and element.get("type") == "textpart"


def has_textpart(element):
    for child in element.iter():
        if child is not element and is_textpart(child):
            return True
    return False


def walk(element, prefix, out):
    parts = []
    for child in element:
        if is_textpart(child):
            parts.append(child)
    if not parts and not has_textpart(element):
        out.append((".".join(prefix), extract.text_of(element)))
        return
    if not parts:
        for child in element:
            walk(child, prefix, out)
        return
    for child in parts:
        walk(child, prefix + [child.get("n")], out)


def leaves(path):
    if not os.path.exists(path):
        sys.exit(f"Missing {path}. Run: python rival_witnesses/fetch_texts.py")
    root = ET.parse(path).getroot()
    body = root.find(f".//{NS}body")
    out = []
    walk(body, [], out)
    return out


def inside_ref(ref, wanted):
    return ref == wanted or ref.startswith(wanted + ".")


def find_sequence(words, sequence, start):
    for index in range(start, len(words) - len(sequence) + 1):
        if words[index:index + len(sequence)] == sequence:
            return index
    return -1


def segment(row):
    """The words (and the ref of each word) of one line of witnesses.txt."""
    name, tier, path, first, last, opening, closing = row
    units = leaves(os.path.join(KIT, path))
    words = []
    refs = []
    taking = first == "-"
    for ref, unit in units:
        if not taking and inside_ref(ref, first):
            taking = True
        if taking:
            for word in unit:
                words.append(word)
                refs.append(ref)
        if taking and last != "-" and inside_ref(ref, last):
            following = units.index((ref, unit)) + 1
            if following >= len(units) or not inside_ref(units[following][0], last):
                break
    if not words:
        sys.exit(f"No text found for {name} {first}-{last} in {path}")
    if opening != "-":
        begin = find_sequence(words, normalised(opening), 0)
        if begin < 0:
            sys.exit(f"Start words not found for {name} {first}: {opening}")
        words = words[begin:]
        refs = refs[begin:]
    if closing != "-":
        ending = normalised(closing)
        end = find_sequence(words, ending, 0)
        if end < 0:
            sys.exit(f"End words not found for {name} {last}: {closing}")
        words = words[:end + len(ending)]
        refs = refs[:end + len(ending)]
    return name, tier, words, refs


def read_nt():
    paul = {}
    other = set()
    for path in sorted(glob(os.path.join(SBLGNT, "*-morphgnt.txt"))):
        book = os.path.basename(path).split("-")[1]
        stream = []
        with open(path, encoding="utf8") as file:
            for line in file:
                columns = line.split()
                word = extract.norm(columns[4])
                if word:
                    stream.append((word, f"{book} {int(columns[0][2:4])}:{int(columns[0][4:6])}"))
        for index in range(len(stream) - SIZE + 1):
            pieces = []
            for item in stream[index:index + SIZE]:
                pieces.append(item[0])
            gram = " ".join(pieces)
            if book in PAUL:
                paul.setdefault(gram, [])
                if stream[index][1] not in paul[gram]:
                    paul[gram].append(stream[index][1])
            else:
                other.add(gram)
    if not paul:
        sys.exit(f"No MorphGNT files in '{SBLGNT}'. Run setup_data.py first.")
    return paul, other


def read_lxx():
    if not os.path.exists(LXX):
        sys.exit(f"Missing {LXX}. Run setup_data.py first.")
    words = []
    with open(LXX, encoding="utf8") as file:
        for row in csv.reader(file, delimiter="\t"):
            if len(row) > 2:
                word = extract.norm(row[2])
                if word:
                    words.append(word)
    grams = set()
    for index in range(len(words) - SIZE + 1):
        grams.add(" ".join(words[index:index + SIZE]))
    return grams


def runs_of(words, refs, paul, lxx, other):
    found = []
    index = 0
    while index <= len(words) - SIZE:
        gram = " ".join(words[index:index + SIZE])
        if gram in paul and gram not in lxx:
            end = index + SIZE
            verses = list(paul[gram])
            elsewhere = gram in other
            while end <= len(words) - 1:
                following = " ".join(words[end - SIZE + 1:end + 1])
                if following in paul and following not in lxx:
                    for verse in paul[following]:
                        if verse not in verses:
                            verses.append(verse)
                    if following in other:
                        elsewhere = True
                    end += 1
                else:
                    break
            found.append((refs[index], " ".join(words[index:end]), verses, elsewhere))
            index = end
        else:
            index += 1
    return found


def mentions_of(words, refs):
    found = []
    for index in range(len(words)):
        word = words[index]
        if word.startswith("παυλ") or word.startswith("αποστολ"):
            begin = max(0, index - CONTEXT)
            found.append((refs[index], word, " ".join(words[begin:index + CONTEXT + 1])))
    return found


def step_one():
    paul, other = read_nt()
    lxx = read_lxx()
    out = ["# Candidates for hand-coding", ""]
    out.append("Made by rival_witnesses.py. Every 4-word sequence a Greek witness shares with Paul's 13 letters and not "
               "found in the LXX, joined into runs, and every mention of Paul or \"the apostle\". \"also elsewhere in "
               "the NT\" marks a run whose wording occurs outside Paul too. Every line is coded by hand in codes.txt.")
    out.append("")
    totals = {}
    for row in read_lines(WITNESSES):
        name, tier, words, refs = segment(row)
        totals.setdefault((name, tier), 0)
        totals[(name, tier)] += len(words)
        runs = runs_of(words, refs, paul, lxx, other)
        mentions = mentions_of(words, refs)
        if not runs and not mentions:
            continue
        out.append(f"## {name} (tier {tier}), {row[2].split('/')[-1]} {row[3]}-{row[4]}")
        out.append("")
        for ref, text, verses, elsewhere in runs:
            note = ""
            if elsewhere:
                note = " (also elsewhere in the NT)"
            out.append(f"- {ref}: {text} ~ {', '.join(verses[:6])}{note}")
        for ref, word, context in mentions:
            out.append(f"- {ref}: mention \"{word}\": ... {context} ...")
        out.append("")
    out.append("## Words searched")
    out.append("")
    out.append("| witness | tier | words |")
    out.append("|---|---|---|")
    for (name, tier), count in totals.items():
        out.append(f"| {name} | {tier} | {count:,} |")
    with open(CANDIDATES, "w", encoding="utf8") as file:
        file.write("\n".join(out) + "\n")
    print(f"Written: {CANDIDATES}")
    return totals


def class_of_verse(book, place):
    if book in PASTORALS:
        return "D"
    for span_book, first, last in ABSENT:
        if span_book == book and first <= place <= last:
            return "B"
    for span_book, first, last in PROBABLY_ABSENT:
        if span_book == book and first <= place <= last:
            return "C"
    return "A"


def class_of_reference(text):
    changed = text.endswith("*")
    if changed:
        text = text[:-1]
    book, place = text.split()
    if book not in PAUL:
        sys.exit(f"Not a letter of Paul in codes.txt: {text}")
    if changed:
        return "B"
    chapter, verses = place.split(":")
    first = verses
    last = verses
    if "-" in verses:
        first, last = verses.split("-")
    found = []
    for verse in range(int(first), int(last) + 1):
        found.append(class_of_verse(book, (int(chapter), verse)))
    for label in ["B", "C", "D"]:
        if label in found:
            return label
    return "A"


def step_two(totals):
    uses = []
    for fields in read_lines(CODES):
        while len(fields) < 7:
            fields.append("")
        witness, tier, place, references, grade, basis, note = fields[:7]
        if grade not in GRADES:
            sys.exit(f"Unknown grade '{grade}' in codes.txt: {witness} {place}")
        classes = []
        for reference in references.split(";"):
            label = class_of_reference(reference.strip())
            if label not in classes:
                classes.append(label)
        uses.append({"witness": witness, "tier": tier, "place": place, "references": references, "grade": grade,
                     "basis": basis, "note": note, "classes": classes})
    out = ["# Paul outside Marcion's circle, to about 160: results", ""]
    out.append("Rules: PREDICTIONS.md (SHA-256 176087ea…13b7db) and AMENDMENTS.md. Uses: codes.txt, coded by hand from "
               "CANDIDATES.md and, for non-Greek texts, from translations. Coding by Claude (an AI model), for review.")
    out.append("")
    out.append("## 1. Uses by witness, grade and class")
    out.append("")
    out.append("Q named, V verbatim, A allusion, D doubtful. An entry citing passages of two classes counts under both.")
    out.append("")
    out.append("| witness | tier | words searched | Q | V | A | D | to class B or C (Q-A) | to class D (Q-A) |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    names = []
    for use in uses:
        if (use["witness"], use["tier"]) not in names:
            names.append((use["witness"], use["tier"]))
    for name, tier in names:
        cells = []
        for grade in GRADES:
            count = 0
            for use in uses:
                if use["witness"] == name and use["grade"] == grade:
                    count += 1
            cells.append(str(count))
        gaps = 0
        pastorals = 0
        for use in uses:
            if use["witness"] == name and use["grade"] in ["Q", "V", "A"]:
                if "B" in use["classes"] or "C" in use["classes"]:
                    gaps += 1
                if "D" in use["classes"]:
                    pastorals += 1
        searched = "translation"
        if (name, tier) in totals:
            searched = f"{totals[(name, tier)]:,}"
        out.append(f"| {name} | {tier} | {searched} | " + " | ".join(cells) + f" | {gaps} | {pastorals} |")
    out.append("")
    out.append("## 2. Every use")
    out.append("")
    for name, tier in names:
        out.append(f"**{name}** (tier {tier})")
        out.append("")
        for use in uses:
            if use["witness"] == name:
                note = ""
                if use["note"]:
                    note = f": {use['note']}"
                out.append(f"- {use['place']} ~ {use['references']}: {use['grade']}, class "
                           f"{'/'.join(use['classes'])}, {use['basis']}{note}")
        out.append("")
    out.append("## 3. Predictions")
    out.append("")
    strong_tier_one = []
    named = {}
    for use in uses:
        if use["tier"] == "1" and use["grade"] in ["Q", "V"] and use["witness"] not in strong_tier_one:
            strong_tier_one.append(use["witness"])
        if use["grade"] == "Q":
            named.setdefault(use["witness"], [])
            for reference in use["references"].split(";"):
                book = reference.strip().split()[0]
                if book not in named[use["witness"]]:
                    named[use["witness"]].append(book)
    tier_one_gaps = []
    tier_two_gaps = []
    for use in uses:
        outside = "B" in use["classes"] or "C" in use["classes"] or "D" in use["classes"]
        if use["tier"] == "1" and outside and use["grade"] in ["Q", "V", "A"]:
            tier_one_gaps.append(use)
        if use["tier"] == "2" and outside and use["grade"] in ["Q", "V"]:
            tier_two_gaps.append(use)
    justin_named = False
    for use in uses:
        if use["witness"] == "Justin" and use["grade"] == "Q":
            justin_named = True
    ptolemy_letters = named.get("Ptolemy", [])
    rows = [
        ("1. At least 3 of the 5 tier-1 witnesses have a Q or V use", len(strong_tier_one) >= 3,
         f"{len(strong_tier_one)}: {', '.join(strong_tier_one)}"),
        ("2. Ptolemy names Paul or the apostle and quotes at least two letters", len(ptolemy_letters) >= 2,
         f"named uses from {len(ptolemy_letters)} letters: {', '.join(ptolemy_letters)}"),
        ("3. A tier-1 Q, V or A use of class B, C or D", len(tier_one_gaps) >= 1, f"{len(tier_one_gaps)} found"),
        ("4. Tier 2 has at least 3 Q or V uses of class B, C or D", len(tier_two_gaps) >= 3,
         f"{len(tier_two_gaps)} found"),
        ("5. Justin never names Paul", not justin_named, justin_detail(justin_named)),
    ]
    out.append("| prediction | met? | detail |")
    out.append("|---|---|---|")
    for text, met, detail in rows:
        word = "not met"
        if met:
            word = "met"
        out.append(f"| {text} | {word} | {detail} |")
    out.append("")
    out.append("## 4. Decision rule")
    out.append("")
    good = []
    hints = []
    for use in tier_one_gaps:
        if "B" in use["classes"] or "C" in use["classes"]:
            if use["grade"] in ["Q", "V"]:
                good.append(use)
            else:
                hints.append(use)
    if good:
        out.append("A tier-1 witness uses a passage Marcion's edition lacked, graded Q or V: good evidence that a "
                   "fuller Paul was in his rivals' hands by about 160.")
        for use in good:
            out.append(f"- {use['witness']} {use['place']} ~ {use['references']} ({use['grade']})")
    elif hints:
        out.append("No tier-1 use of a passage Marcion's edition lacked is graded Q or V. Grade A only, a hint:")
        for use in hints:
            out.append(f"- {use['witness']} {use['place']} ~ {use['references']} ({use['grade']})")
    else:
        out.append("No tier-1 use of a passage Marcion's edition lacked: consistent with Marcion's edition being the "
                   "Paul that spread. A point for Livesey's model.")
    pastoral_uses = []
    for use in tier_one_gaps:
        if "D" in use["classes"]:
            pastoral_uses.append(use)
    out.append("")
    out.append(f"Tier-1 uses of the Pastorals (class D, Q to A): {len(pastoral_uses)}.")
    out.append("")
    out.append("Named uses (Q) by groups outside Marcion's circle: " + "; ".join(
        named_summary(named)) + ".")
    with open(RESULTS, "w", encoding="utf8") as file:
        file.write("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"Written: {RESULTS}")


def justin_detail(justin_named):
    if justin_named:
        return "named use found"
    return "no named use"


def named_summary(named):
    parts = []
    for witness, books in named.items():
        parts.append(f"{witness} ({', '.join(books)})")
    if not parts:
        parts.append("none")
    return parts


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    totals = step_one()
    if os.path.exists(CODES):
        step_two(totals)
    else:
        print("No codes.txt yet: code CANDIDATES.md by hand, then run again.")


if __name__ == "__main__":
    main()
