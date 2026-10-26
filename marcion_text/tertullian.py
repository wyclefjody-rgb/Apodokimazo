"""
    Part B of marcion_text/PREDICTIONS.md: what Tertullian says stood in Marcion's own edition of Paul.

    1. Fetches the Latin of Tertullian, Against Marcion (Oehler's edition, Perseus canonical-latinLit stoa0275.stoa006)
       with a sparse git clone, if it is not already in the kit, and extracts Book 5 chapter by chapter into
       marcion_text/adv_marc_5.txt. The Perseus file has no division for chapter 9; it is split off at Oehler's own
       marker "Cap. IX.".
    2. Reads the hand codes in tertullian_codes.txt and checks every one: the fields are valid and the Latin anchor
       occurs in the chapter named.
    3. Lists the references to Paul that Oehler printed in Book 5 and that no code covers in the same chapter, so a
       reviewer can see what was left out.
    4. Tallies the codes and applies the decision rule of PREDICTIONS.md section 4.

    Output: TERTULLIAN.md and adv_marc_5.txt (local data; keep both texts out of public uploads).

    Usage (from the kit folder):   python -X utf8 marcion_text/tertullian.py
"""
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
LATIN = os.path.join(KIT, "canonical-latinLit")
REPO = "https://github.com/PerseusDL/canonical-latinLit.git"
FOLDER = "/data/stoa0275/stoa006/"
XML = os.path.join(LATIN, "data", "stoa0275", "stoa006", "stoa0275.stoa006.opp-lat1.xml")
TEXT = os.path.join(HERE, "adv_marc_5.txt")
CODES = os.path.join(HERE, "tertullian_codes.txt")
OUTPUT = os.path.join(HERE, "TERTULLIAN.md")
TEI = "{http://www.tei-c.org/ns/1.0}"

LETTERS = ["Ga", "1Co", "2Co", "Ro", "1Th", "2Th", "Eph", "Col", "Php", "Phm"]
STATUS = ["in", "changed", "unclear"]
BEARING = ["face", "argument", "neutral"]
STRENGTH = ["strong", "medium", "weak"]
ATTESTED = ["explicit", "implicit"]
OEHLER_BOOKS = [("II ?Thess", "2Th"), ("I ?Thes[sa]", "1Th"), ("II ?Cor", "2Co"), ("M Cor", "2Co"), ("I ?C[oe]r", "1Co"),
                ("R[oe]m", "Ro"), ("Ephes", "Eph"), ("Eph", "Eph"), ("Ph[il]l", "Php"), ("Gal", "Ga"), ("Ga", "Ga"),
                ("Co[lIt]", "Col")]
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}


def fetch():
    """Sparse-clones canonical-latinLit with only Against Marcion, unless the file is already there."""
    if os.path.exists(XML):
        return
    if not os.path.isdir(os.path.join(LATIN, ".git")):
        subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", REPO, LATIN], check=True)
        subprocess.run(["git", "sparse-checkout", "set", "--no-cone", FOLDER], cwd=LATIN, check=True)
    else:
        subprocess.run(["git", "sparse-checkout", "add", FOLDER], cwd=LATIN, check=True)
    if not os.path.exists(XML):
        sys.exit(f"Could not find {XML} after cloning.")


def walk(element, buffers, refs):
    """Collects the text of a chapter in document order, starting a new buffer at Oehler's "Cap. IX." marker."""
    if element.text:
        buffers[-1].append(element.text)
    for child in element:
        if child.tag == TEI + "bibl":
            label = child.get("n") or ""
            if label.strip() == "Cap. IX.":
                buffers.append([])
                refs.append([])
            else:
                refs[-1].append(label)
        else:
            walk(child, buffers, refs)
        if child.tail:
            buffers[-1].append(child.tail)


def book_five():
    """Returns a list of (chapter label, text, Oehler references) for Against Marcion book 5."""
    root = ET.parse(XML).getroot()
    book = None
    for div in root.iter(TEI + "div"):
        if div.get("subtype") == "book" and div.get("n") == "5":
            book = div
    if book is None:
        sys.exit("Book 5 not found in the Perseus file.")
    chapters = []
    for div in book:
        if div.get("subtype") != "chapter":
            continue
        buffers = [[]]
        refs = [[]]
        walk(div, buffers, refs)
        number = int(div.get("n"))
        for index in range(len(buffers)):
            text = " ".join("".join(buffers[index]).split())
            chapters.append((f"5.{number + index}", text, refs[index]))
    labels = []
    for label, text, found in chapters:
        labels.append(label)
    if "5.9" not in labels:
        sys.exit("Oehler's 'Cap. IX.' marker was not found; the chapter numbering would be wrong.")
    return chapters


def read_codes():
    codes = []
    with open(CODES, encoding="utf8") as file:
        for number, line in enumerate(file, 1):
            if line.startswith("#") or not line.strip():
                continue
            fields = re.split(r"\s+\|\s+", line.rstrip("\n"), maxsplit=7)
            if len(fields) != 8:
                sys.exit(f"Line {number}: expected 8 fields, found {len(fields)}")
            passage, status, bearing, strength, attested, chapter, anchor, reason = fields
            problems = []
            if passage.split(" ")[0] not in LETTERS:
                problems.append(f"letter '{passage.split(' ')[0]}'")
            if status not in STATUS:
                problems.append(f"status '{status}'")
            if bearing not in BEARING:
                problems.append(f"bearing '{bearing}'")
            if bearing == "face" and strength not in STRENGTH:
                problems.append(f"strength '{strength}' for a face code")
            if bearing != "face" and strength != "-":
                problems.append(f"strength '{strength}' for a {bearing} code")
            if status == "in" and attested not in ATTESTED:
                problems.append(f"attested '{attested}' for an 'in' code")
            if status != "in" and attested != "-":
                problems.append(f"attested '{attested}' for a '{status}' code")
            if problems:
                sys.exit(f"Line {number} ({passage}): bad " + ", ".join(problems))
            codes.append({"passage": passage, "status": status, "bearing": bearing, "strength": strength,
                          "attested": attested, "chapter": chapter, "anchor": anchor, "reason": reason})
    return codes


def chapters_of(passage):
    """Returns (letter, first chapter, last chapter) for a passage such as 'Ro 8:12-10:1' or 'Ga 3:6-9'."""
    letter, rest = passage.split(" ", 1)
    parts = rest.split(" ")[0].split("-")
    first = int(re.match(r"\d+", parts[0]).group())
    last = first
    for part in parts[1:]:
        if ":" in part or ":" not in parts[0]:
            last = int(re.match(r"\d+", part).group())
    return letter, first, last


def roman(numeral):
    total = 0
    previous = 0
    for letter in reversed(numeral):
        value = ROMAN[letter]
        if value < previous:
            total -= value
        else:
            total += value
            previous = value
    return total


def oehler_paul(label):
    """Finds the references to Paul's ten letters in one of Oehler's marginal labels, as (letter, chapter)."""
    found = []
    names = []
    for name, short in OEHLER_BOOKS:
        names.append(name)
    pattern = r"\b(" + "|".join(names) + r")\.?\s*([IVXL]+)\b"
    for match in re.finditer(pattern, label):
        for name, short in OEHLER_BOOKS:
            if re.fullmatch(name, match.group(1)):
                found.append((short, roman(match.group(2))))
                break
    return found


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fetch()
    chapters = book_five()
    texts = {}
    with open(TEXT, "w", encoding="utf8") as file:
        for label, text, refs in chapters:
            texts[label] = text
            file.write(f"[{label}] {text}\n\n")
    codes = read_codes()
    missing = []
    for code in codes:
        if code["chapter"] not in texts:
            missing.append(f"{code['passage']}: no chapter {code['chapter']}")
        elif code["anchor"] not in texts[code["chapter"]]:
            missing.append(f"{code['passage']}: anchor not in {code['chapter']}: '{code['anchor']}'")
    if missing:
        sys.exit("Anchor check failed:\n  " + "\n  ".join(missing))

    uncovered = []
    for label, text, refs in chapters:
        for ref in refs:
            for letter, number in oehler_paul(ref):
                covered = False
                for code in codes:
                    if code["chapter"] != label:
                        continue
                    code_letter, first, last = chapters_of(code["passage"])
                    if code_letter == letter and first <= number <= last:
                        covered = True
                if not covered:
                    uncovered.append(f"| {label} | {ref.strip()} |")

    table = {}
    for status in STATUS:
        for bearing in BEARING:
            table[(status, bearing)] = 0
    for code in codes:
        table[(code["status"], code["bearing"])] += 1
    face_in = []
    for code in codes:
        if code["status"] == "in" and code["bearing"] == "face":
            face_in.append(code)
    tiers = [("all strengths", STRENGTH, ATTESTED), ("strong and medium", ["strong", "medium"], ATTESTED),
             ("strong only", ["strong"], ATTESTED), ("explicitly attested, any strength", STRENGTH, ["explicit"])]

    lines = ["# What Tertullian says stood in Marcion's edition (Part B)", "",
             "Rules: PREDICTIONS.md sections 3-4 (SHA-256 3c8dfa4b…c3c7). Generated by tertullian.py from "
             "tertullian_codes.txt. Latin: Oehler (1854), Perseus canonical-latinLit stoa0275.stoa006. "
             "Every code's Latin anchor was found in the chapter it names.", "",
             f"Codes: {len(codes)} passages.", "", "## Status and bearing", "",
             "| status | against on its face | against by Tertullian's argument | neutral or for Marcion | total |",
             "|---|---|---|---|---|"]
    for status in STATUS:
        row_total = 0
        row = f"| {status} |"
        for bearing in BEARING:
            row += f" {table[(status, bearing)]} |"
            row_total += table[(status, bearing)]
        lines.append(row + f" {row_total} |")
    lines.append("")
    lines.append("## Decision rule: passages in Marcion's text and against Marcion's theology on their face")
    lines.append("")
    lines.append("Pre-registered threshold: 10 or more counts as clear evidence against Marcionite composition.")
    lines.append("")
    lines.append("| counting | passages | meets the threshold of 10? |")
    lines.append("|---|---|---|")
    for name, strengths, attestations in tiers:
        count = 0
        for code in face_in:
            if code["strength"] in strengths and code["attested"] in attestations:
                count += 1
        lines.append(f"| {name} | {count} | {'yes' if count >= 10 else 'no'} |")
    lines.append("")
    lines.append("| passage | strength | attested | chapter | why |")
    lines.append("|---|---|---|---|---|")
    for code in face_in:
        lines.append(f"| {code['passage']} | {code['strength']} | {code['attested']} | {code['chapter']} | "
                     f"{code['reason']} |")
    lines.append("")
    lines.append("## By letter")
    lines.append("")
    lines.append("| letter | in | of which face | changed | unclear |")
    lines.append("|---|---|---|---|---|")
    for letter in LETTERS:
        counts = {"in": 0, "face": 0, "changed": 0, "unclear": 0}
        for code in codes:
            if code["passage"].split(" ")[0] != letter:
                continue
            counts[code["status"]] += 1
            if code["status"] == "in" and code["bearing"] == "face":
                counts["face"] += 1
        lines.append(f"| {letter} | {counts['in']} | {counts['face']} | {counts['changed']} | {counts['unclear']} |")
    lines.append("")
    lines.append("## What Tertullian says Marcion removed, added or altered")
    lines.append("")
    lines.append("| passage | bearing of the canonical wording | chapter | what |")
    lines.append("|---|---|---|---|")
    for code in codes:
        if code["status"] == "changed":
            bearing = code["bearing"] if code["bearing"] != "face" else f"face ({code['strength']})"
            lines.append(f"| {code['passage']} | {bearing} | {code['chapter']} | {code['reason']} |")
    lines.append("")
    lines.append("## Unclear")
    lines.append("")
    lines.append("| passage | chapter | why |")
    lines.append("|---|---|---|")
    for code in codes:
        if code["status"] == "unclear":
            lines.append(f"| {code['passage']} | {code['chapter']} | {code['reason']} |")
    lines.append("")
    lines.append("## Oehler's references to Paul with no code in the same chapter")
    lines.append("")
    lines.append("Oehler printed a scripture reference beside each quotation. These are the ones to Paul's ten "
                 "letters that no code covers in that chapter. Most are passing cross-references to another letter; "
                 "any that is a passage Tertullian actually discusses should be added to tertullian_codes.txt.")
    lines.append("")
    if uncovered:
        lines.append("| chapter | Oehler's reference |")
        lines.append("|---|---|")
        lines.extend(uncovered)
    else:
        lines.append("None.")
    lines.append("")
    lines.append("## Every code")
    lines.append("")
    lines.append("| passage | status | bearing | strength | attested | chapter | Latin anchor | reason |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for code in codes:
        lines.append(f"| {code['passage']} | {code['status']} | {code['bearing']} | {code['strength']} | "
                     f"{code['attested']} | {code['chapter']} | {code['anchor']} | {code['reason']} |")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    stop = lines.index("## By letter")
    print("\n".join(lines[:stop]))
    print(f"\nOehler references to Paul not covered by a code: {len(uncovered)} (listed in TERTULLIAN.md)")
    print(f"Wrote {OUTPUT}\nWrote {TEXT}")


if __name__ == "__main__":
    main()
