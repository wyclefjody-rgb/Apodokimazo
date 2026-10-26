"""
    The Last Supper wording: Mark 14, Matthew 26, Luke 22 and 1 Corinthians 11, with Justin (First Apology 66.3),
    the Didache (9-10) and Marcion's gospel as Tertullian reports it (Against Marcion 4.40). Rules in
    borrowing/PREDICTIONS.md (SHA-256 35906bca…198e), section 3.

    Plain word forms (lower case, accents removed) are compared, so that Justin and the Didache, which have no
    lemma tagging, can be set beside the New Testament.

    Needs sblgnt/, First1KGreek/ (tlg0645 Justin, tlg1311 Didache) and canonical-latinLit/ (stoa0275, from
    marcion_text/tertullian.py). Run borrowing/fetch_texts.py first if any is missing. Output: SUPPER.md.

    Usage (from the kit folder):   python -X utf8 borrowing/supper.py
"""
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
JUSTIN = os.path.join(KIT, "First1KGreek", "data", "tlg0645", "tlg001", "tlg0645.tlg001.1st1K-grc1.xml")
DIDACHE = os.path.join(KIT, "First1KGreek", "data", "tlg1311", "tlg001", "tlg1311.tlg001.1st1K-grc1.xml")
TERTULLIAN = os.path.join(KIT, "canonical-latinLit", "data", "stoa0275", "stoa006", "stoa0275.stoa006.opp-lat1.xml")
OUTPUT = os.path.join(HERE, "SUPPER.md")
TEI = "{http://www.tei-c.org/ns/1.0}"
CANONICAL = ["Mark 14:22-25", "Matthew 26:26-29", "Luke 22:15-20", "1 Corinthians 11:23-26"]
KEY_WORDS = [("body", "σωμα"), ("blood", "αιμα"), ("remembrance", "αναμνησιν"), ("covenant", "διαθηκη"),
             ("new", "καινη"), ("for you", "υπερ υμων"), ("after supper", "μετα το δειπνησαι"),
             ("do this", "τουτο ποιειτε")]


def verses(book, chapter, first, last):
    paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
    if not paths:
        sys.exit(f"No MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
    words = []
    with open(paths[0], encoding="utf8") as file:
        for line in file:
            columns = line.split()
            if int(columns[0][2:4]) == chapter and first <= int(columns[0][4:6]) <= last:
                word = extract.norm(columns[4])
                if word:
                    words.append(word)
    return words


def chapter_words(path, wanted):
    if not os.path.exists(path):
        sys.exit(f"Missing {path}. Run: python borrowing/fetch_texts.py")
    body = ET.parse(path).getroot().find(f".//{TEI}body")
    words = []
    for div in body.iter(TEI + "div"):
        if div.get("subtype") == "chapter" and div.get("n") in wanted:
            words.extend(extract.text_of(div))
    return words


def between(words, start, end):
    """The words from the first occurrence of the start sequence to the end of the first end sequence after it."""
    for index in range(len(words) - len(start) + 1):
        if words[index:index + len(start)] == start:
            for stop in range(index, len(words) - len(end) + 1):
                if words[stop:stop + len(end)] == end:
                    return words[index:stop + len(end)]
    sys.exit(f"Could not find '{' '.join(start)}' ... '{' '.join(end)}'")


def grams(words, size):
    found = set()
    for index in range(len(words) - size + 1):
        found.add(" ".join(words[index:index + size]))
    return found


def has(words, phrase):
    return phrase in " ".join(words)


def latin_chapter(book, number):
    if not os.path.exists(TERTULLIAN):
        sys.exit(f"Missing {TERTULLIAN}. Run marcion_text/tertullian.py or borrowing/fetch_texts.py first.")
    root = ET.parse(TERTULLIAN).getroot()
    for div in root.iter(TEI + "div"):
        if div.get("subtype") == "book" and div.get("n") == book:
            for chapter in div:
                if chapter.get("n") == number:
                    pieces = []
                    for text in chapter.itertext():
                        pieces.append(text)
                    return " ".join(" ".join(pieces).split())
    sys.exit(f"Against Marcion {book}.{number} not found")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    texts = {
        "Mark 14:22-25": verses("Mk", 14, 22, 25),
        "Matthew 26:26-29": verses("Mt", 26, 26, 29),
        "Luke 22:15-20": verses("Lk", 22, 15, 20),
        "1 Corinthians 11:23-26": verses("1Co", 11, 23, 26),
    }
    parts = {
        "Mark 14:22-24": verses("Mk", 14, 22, 24),
        "Mark 14:25": verses("Mk", 14, 25, 25),
        "Luke 22:15-18": verses("Lk", 22, 15, 18),
        "Luke 22:19-20": verses("Lk", 22, 19, 20),
        "1 Corinthians 11:23-25": verses("1Co", 11, 23, 25),
    }
    luke = verses("Lk", 22, 15, 19)
    short = between(luke, luke[:2], ["το", "σωμα", "μου"])
    parts["Luke, shorter text (22:15-19a)"] = short
    justin = between(chapter_words(JUSTIN, ["66"]), ["τον", "ιησουν", "λαβοντα"], ["το", "αιμα", "μου"])
    didache = chapter_words(DIDACHE, ["9", "10"])
    others = {"Justin, First Apology 66.3": justin, "Didache 9-10": didache}

    lines = ["# The Last Supper wording", "",
             "Rules: PREDICTIONS.md (SHA-256 35906bca28a5a63f40a45f653c990052b9eb54b6608c7ea302433f464a5b198e), "
             "section 3. Generated by supper.py. Plain word forms, accents removed.", "",
             "## 1. The four canonical accounts, pair by pair", "",
             "| pair | shared 2-word sequences | shared 3-word sequences |", "|---|---|---|"]
    pairs = []
    for index, first in enumerate(CANONICAL):
        for second in CANONICAL[index + 1:]:
            two = grams(texts[first], 2) & grams(texts[second], 2)
            three = grams(texts[first], 3) & grams(texts[second], 3)
            pairs.append((len(three), len(two), first, second))
            lines.append(f"| {first} / {second} | {len(two)} | {len(three)} |")
    pairs.sort(reverse=True)
    lines.append("")
    lines.append(f"Most shared 3-word sequences: {pairs[0][2]} / {pairs[0][3]} ({pairs[0][0]}).")
    lines.append("")
    lines.append("### Agreements found in exactly two of the four accounts (2-word sequences)")
    lines.append("")
    owners = {}
    for name in CANONICAL:
        for gram in grams(texts[name], 2):
            owners.setdefault(gram, []).append(name)
    grouped = {}
    for gram, names in owners.items():
        if len(names) == 2:
            grouped.setdefault(" + ".join(names), []).append(gram)
    lines.append("| accounts | count | sequences |")
    lines.append("|---|---|---|")
    for key in sorted(grouped):
        lines.append(f"| {key} | {len(grouped[key])} | {'; '.join(sorted(grouped[key]))} |")
    lines.append("")
    lines.append("## 2. Luke's parts against Mark and Paul")
    lines.append("")
    lines.append("| Luke | compared with | shared 2-word | shared 3-word | the 3-word sequences |")
    lines.append("|---|---|---|---|---|")
    for luke_part, targets in [("Luke 22:19-20", ["Mark 14:22-24", "1 Corinthians 11:23-25"]),
                               ("Luke 22:15-18", ["Mark 14:25", "1 Corinthians 11:23-25"]),
                               ("Luke, shorter text (22:15-19a)", ["Mark 14:22-24", "1 Corinthians 11:23-25"])]:
        for target in targets:
            two = grams(parts[luke_part], 2) & grams(parts[target], 2)
            three = grams(parts[luke_part], 3) & grams(parts[target], 3)
            lines.append(f"| {luke_part} | {target} | {len(two)} | {len(three)} | {'; '.join(sorted(three))} |")
    lines.append("")
    lines.append("## 3. Key wording in every account")
    lines.append("")
    header = "| text |"
    rule = "|---|"
    for label, phrase in KEY_WORDS:
        header += f" {label} |"
        rule += "---|"
    lines.append(header)
    lines.append(rule)
    every = {}
    every.update(texts)
    every["Luke, shorter text (22:15-19a)"] = short
    every.update(others)
    for name, words in every.items():
        row = f"| {name} |"
        for label, phrase in KEY_WORDS:
            row += f" {'yes' if has(words, phrase) else ''} |"
        lines.append(row)
    lines.append("")
    lines.append("## 4. Justin and the Didache against each canonical account")
    lines.append("")
    lines.append("| text | compared with | shared 2-word | shared 3-word | the 3-word sequences |")
    lines.append("|---|---|---|---|---|")
    for name, words in others.items():
        for target in CANONICAL:
            two = grams(words, 2) & grams(texts[target], 2)
            three = grams(words, 3) & grams(texts[target], 3)
            lines.append(f"| {name} | {target} | {len(two)} | {len(three)} | {'; '.join(sorted(three))} |")
    lines.append("")
    lines.append(f"Justin's words as extracted: {' '.join(justin)}")
    lines.append("")
    lines.append("## 5. Marcion's gospel: Tertullian, Against Marcion 4.40")
    lines.append("")
    lines.append("Sentences of 4.40 that mention the bread, the body, the cup, the blood or the covenant (Latin):")
    lines.append("")
    text = latin_chapter("4", "40")
    for sentence in re.split(r"(?<=[.?!])\s+", text):
        lowered = sentence.lower()
        for word in ["corpus", "calic", "sanguin", "testament", "panem", "commemor"]:
            if word in lowered:
                lines.append(f"- {sentence}")
                break
    lines.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
