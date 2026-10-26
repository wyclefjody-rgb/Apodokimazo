"""
    Slip-rate study, step 1: find candidate datable passages (AMENDMENTS.md 2).

    Every text is searched with the terms of topics.txt. Hits in the same verse (New Testament) or section (other
    texts) form one candidate passage. Output: CANDIDATES.md (every candidate with its text, for reading and coding)
    and the word count of each text.

    Needs: sblgnt/ and First1KGreek/ with tlg1443, tlg1271 (setup_data.py) and tlg0317, tlg2038, tlg2949
    (python slip_rate/fetch_texts.py).

    Usage (from the kit folder):   python -X utf8 slip_rate/candidates.py
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(KIT, "paul_lineup"))
sys.path.insert(0, os.path.join(KIT, "advanced"))
from words import keep_accents, plain
import extract

SBLGNT = os.path.join(KIT, "sblgnt")
FIRST1K = os.path.join(KIT, "First1KGreek", "data")
TOPICS = os.path.join(HERE, "topics.txt")
OUTPUT = os.path.join(HERE, "CANDIDATES.md")
NS = "{http://www.tei-c.org/ns/1.0}"

TEXTS = [
    ("core four", "test", [("nt", "Ro"), ("nt", "1Co"), ("nt", "2Co"), ("nt", "Ga")]),
    ("Pastorals", "A", [("nt", "1Ti"), ("nt", "2Ti"), ("nt", "Tit")]),
    ("spurious Ignatius", "A", [("first1k", "tlg1443", "tlg002", ["13", "1", "4", "5", "9", "10"])]),
    ("Clementine letters to James", "A", [("first1k", "tlg1271", "tlg003", None),
                                          ("first1k", "tlg1271", "tlg004", None),
                                          ("first1k", "tlg1271", "tlg005", None)]),
    ("2 Peter", "B", [("nt", "2Pe")]),
    ("Acts of John", "B", [("first1k", "tlg0317", "tlg001", None)]),
    ("Acts of Thomas", "B", [("first1k", "tlg2038", "tlg001", None)]),
    ("Acts of Barnabas", "B", [("first1k", "tlg2949", "tlg001", None)]),
]
LETTER_NAMES = {"13": "Mary to Ignatius", "1": "To Mary", "4": "Tarsians", "5": "Philippians", "9": "Antiochenes",
                "10": "Hero"}
WORK_NAMES = {"tlg003": "Peter to James", "tlg004": "Contestatio", "tlg005": "Clement to James"}


def read_topics():
    topics = []
    with open(TOPICS, encoding="utf8") as file:
        for line in file:
            if line.startswith("#") or not line.strip():
                continue
            name, terms = line.split("|", 1)
            prefixes = []
            exact = set()
            for term in terms.split(","):
                term = term.strip()
                if term.startswith("="):
                    exact.add(term[1:])
                elif term:
                    prefixes.append(term)
            topics.append((name.strip(), prefixes, exact))
    return topics


def form(word):
    return plain(keep_accents(word))


def nt_passages(book):
    paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
    if not paths:
        sys.exit(f"No MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
    verses = []
    with open(paths[0], encoding="utf8") as file:
        for line in file:
            columns = line.split()
            place = f"{book} {int(columns[0][2:4])}:{int(columns[0][4:6])}"
            if not verses or verses[-1][0] != place:
                verses.append((place, [], []))
            verses[-1][1].append(columns[3])
            verses[-1][2].append(form(columns[4]))
    return verses


def leaves(element):
    """The innermost textpart divisions, each with a label built from its ancestors' numbers."""
    found = []

    def walk(node, label):
        children = []
        for child in node:
            if child.tag == NS + "div" and child.get("type") == "textpart":
                children.append(child)
        if not children:
            found.append((label, node))
            return
        for child in children:
            number = child.get("n", "?")
            walk(child, number if not label else f"{label}.{number}")

    walk(element, "")
    return found


def first1k_passages(author, work, pick):
    paths = glob(os.path.join(FIRST1K, author, work, f"{author}.{work}.1st1K-grc*.xml"))
    if not paths:
        sys.exit(f"No First1KGreek file for {author}.{work}. Run setup_data.py and slip_rate/fetch_texts.py first.")
    body = ET.parse(paths[0]).getroot().find(f".//{NS}body")
    edition = None
    for div in body.iter(NS + "div"):
        if div.get("type") == "edition":
            edition = div
            break
    passages = []
    for label, node in leaves(edition if edition is not None else body):
        top = label.split(".")[0]
        if pick is not None and top not in pick:
            continue
        raw = extract.text_of(node)
        shown = []
        forms = []
        for word in raw:
            shown.append(word)
            forms.append(plain(word))
        if not raw:
            continue
        name = label
        if author == "tlg1443":
            name = LETTER_NAMES[top] + " " + ".".join(label.split(".")[1:])
        if author == "tlg1271":
            name = WORK_NAMES[work] + " " + label
        passages.append((name, shown, forms))
    return passages


def load(sources):
    passages = []
    for source in sources:
        if source[0] == "nt":
            passages.extend(nt_passages(source[1]))
        else:
            passages.extend(first1k_passages(source[1], source[2], source[3]))
    return passages


def hits_in(forms, topics):
    found = []
    for name, prefixes, exact in topics:
        for word in forms:
            matched = word in exact
            for prefix in prefixes:
                if word.startswith(prefix):
                    matched = True
            if matched:
                if name not in found:
                    found.append(name)
                break
    return found


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    extract.norm = keep_accents
    topics = read_topics()
    lines = ["# Candidate datable passages (slip-rate study, step 1)", "",
             "Generated by candidates.py from topics.txt (AMENDMENTS.md 2). Each candidate is coded in codes.txt.", "",
             "| text | group | words | candidates |", "|---|---|---|---|"]
    sections = []
    for name, group, sources in TEXTS:
        passages = load(sources)
        words = 0
        found = []
        for place, shown, forms in passages:
            words += len(forms)
            topics_hit = hits_in(forms, topics)
            if topics_hit:
                found.append((place, topics_hit, " ".join(shown)))
        lines.append(f"| {name} | {group} | {words:,} | {len(found)} |")
        sections.append((name, found))
    lines.append("")
    for name, found in sections:
        lines.append(f"## {name}")
        lines.append("")
        for place, topics_hit, text in found:
            lines.append(f"- **{place}** ({'; '.join(topics_hit)}): {text}")
        lines.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines[:15]))
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
