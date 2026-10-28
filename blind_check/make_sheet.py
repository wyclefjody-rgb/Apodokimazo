"""
    blind_check, step 1: makes the blind sheet (SHEET.md) and its key (key.csv) from the codes of slip_rate,
    third_corinthians and real_letters. Rules in blind_check/PREDICTIONS.md (SHA-256 f7b89d0c…0c4e).

    Give a coder SHEET.md only. Do not show them key.csv, or any of the codes files.

    Usage (from the kit folder):   python -X utf8 blind_check/make_sheet.py
"""
import csv
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
SOURCES = [os.path.join(KIT, "slip_rate", "codes.txt"), os.path.join(KIT, "third_corinthians", "codes.txt"),
           os.path.join(KIT, "real_letters", "codes.txt")]
SHEET = os.path.join(HERE, "SHEET.md")
KEY = os.path.join(HERE, "key.csv")
SEED = 20261027
SETTINGS = {
    "core four": "claims to be written in the 50s CE",
    "Pastorals": "claims to be written in the 60s CE",
    "spurious Ignatius": "claims to be written about 110 CE",
    "Clementine letters to James": "claims to be written in the 60s CE",
    "2 Peter": "claims to be written in the 60s CE",
    "Acts of John": "is set in the late 1st century CE",
    "Acts of Thomas": "is set in the 30s-40s CE",
    "Acts of Barnabas": "is set in the 50s CE",
    "3 Corinthians": "claims to be written in the 50s CE",
    "Pliny": "was written about 98-112 CE",
    "Cicero": "was written 68-61 BCE",
    "Seneca": "was written about 63-65 CE",
}
GROUPS = {
    "core four": "Paul", "Pastorals": "later A", "spurious Ignatius": "later A", "Clementine letters to James":
    "later A", "3 Corinthians": "later A", "2 Peter": "later B", "Acts of John": "later B", "Acts of Thomas":
    "later B", "Acts of Barnabas": "later B", "Pliny": "genuine", "Cicero": "genuine", "Seneca": "genuine",
}
WRITERS = {"core four": "Paul", "3 Corinthians": "Paul", "Pliny": "Pliny", "Cicero": "Cicero", "Seneca": "Seneca",
           "spurious Ignatius": "Ignatius", "Clementine letters to James": "Clement"}


def anonymise(text, source):
    """Replaces the letter-writer's own name only; other people keep their names."""
    if source not in WRITERS:
        return text
    name = WRITERS[source]
    text = re.sub(r"\b" + name + r"'s\b", "the writer's", text)
    return re.sub(r"\b" + name + r"(?![a-z])", "the writer", text)


def read_items():
    items = []
    for path in SOURCES:
        if not os.path.exists(path):
            sys.exit(f"Missing {path}.")
        with open(path, encoding="utf8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                fields = []
                for part in line.split("|"):
                    fields.append(part.strip())
                text, places, item, code = fields[0], fields[1], fields[2], fields[3]
                if code == "not":
                    continue
                if text not in SETTINGS:
                    sys.exit(f"No setting for '{text}'.")
                items.append({"text": text, "places": places, "item": item, "code": code, "strength": fields[4]})
    return items


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items = read_items()
    order = list(range(len(items)))
    random.Random(SEED).shuffle(order)
    lines = ["# Blind coding sheet", "",
             "Each line is one detail from an ancient letter or narrative. For each, decide whether the detail fits "
             "the date given, using any evidence you can find independent of the text itself.", "",
             "- **fits**: fits that date and would be odd later;",
             "- **either**: fits that date and later times too;",
             "- **slip**: fits only a later time (an anachronism, or knowledge of a later event, office, text or "
             "controversy), or is wrong about its own time as independent evidence shows;",
             "- **not**: cannot be checked against independent evidence.", "",
             "Answer with one line per ID: `ID | code | strength (strong, medium or weak, for slips only) | reason`.",
             "", "| ID | the text ... | detail |", "|---|---|---|"]
    with open(KEY, "w", encoding="utf8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "text", "group", "places", "original_code", "original_strength"])
        number = 0
        for index in order:
            number += 1
            item = items[index]
            identifier = f"B{number:03d}"
            detail = anonymise(item["item"], item["text"])
            lines.append(f"| {identifier} | {SETTINGS[item['text']]} | {detail} |")
            writer.writerow([identifier, item["text"], GROUPS[item["text"]], item["places"], item["code"],
                             item["strength"]])
    with open(SHEET, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print(f"{len(items)} items. Written: {SHEET} and {KEY}")


if __name__ == "__main__":
    main()
