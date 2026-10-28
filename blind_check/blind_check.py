"""
    blind_check, step 2: scores blind codings of SHEET.md against the key. Rules in blind_check/PREDICTIONS.md
    (SHA-256 f7b89d0c…0c4e) and AMENDMENTS.md.

    Each coder's answers go in blind_check/coders/<name>.txt, one line per ID:   B001 | code | strength | reason
    The original coding (from key.csv) is scored too, as a reference.

    Output: RESULTS.md.

    Usage (from the kit folder):   python -X utf8 blind_check/blind_check.py
"""
import csv
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = os.path.join(HERE, "key.csv")
CODERS = os.path.join(HERE, "coders")
OUTPUT = os.path.join(HERE, "RESULTS.md")
CODES = ("fits", "either", "slip", "not")
GROUPS = [("genuine", "genuine letters (Pliny, Cicero, Seneca)"),
          ("later A", "Group A + 3 Corinthians"),
          ("later B", "Group B (2 Peter, Acts of John, Thomas, Barnabas)"),
          ("Paul", "Paul's core four")]


def read_key():
    if not os.path.exists(KEY):
        sys.exit(f"Missing {KEY}. Run: python -X utf8 blind_check/make_sheet.py")
    key = {}
    with open(KEY, encoding="utf8") as file:
        for row in csv.DictReader(file):
            key[row["id"]] = row
    return key


def read_coder(path, key):
    codes = {}
    with open(path, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = []
            for part in line.split("|"):
                fields.append(part.strip())
            identifier = fields[0]
            code = fields[1].lower()
            if identifier not in key:
                sys.exit(f"{path}: unknown ID {identifier}")
            if code not in CODES:
                sys.exit(f"{path}: bad code '{code}' for {identifier}")
            codes[identifier] = code
    missing = []
    for identifier in key:
        if identifier not in codes:
            missing.append(identifier)
    if missing:
        sys.exit(f"{path}: {len(missing)} IDs not coded, first {missing[0]}")
    return codes


def group_counts(codes, key):
    counts = {}
    for name, label in GROUPS:
        counts[name] = {"fits": 0, "either": 0, "slip": 0, "not": 0, "items": 0}
    for identifier, code in codes.items():
        group = key[identifier]["group"]
        counts[group][code] += 1
        if code != "not":
            counts[group]["items"] += 1
    return counts


def rate(count):
    if count["items"] == 0:
        return 0.0
    return count["slip"] / count["items"]


def kappa(first, second):
    """Cohen's kappa on slip / not slip over all IDs."""
    both = 0
    only_first = 0
    only_second = 0
    neither = 0
    for identifier in first:
        a = first[identifier] == "slip"
        b = second[identifier] == "slip"
        if a and b:
            both += 1
        elif a:
            only_first += 1
        elif b:
            only_second += 1
        else:
            neither += 1
    total = both + only_first + only_second + neither
    observed = (both + neither) / total
    first_yes = (both + only_first) / total
    second_yes = (both + only_second) / total
    expected = first_yes * second_yes + (1 - first_yes) * (1 - second_yes)
    if expected >= 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def log_beta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def chance_of_record(slips, items, paul_slips, paul_items):
    """Beta-binomial probability of Paul's record (paul_slips in paul_items) given a rate learned from slips in items.
    With paul_slips = 0 it equals real_letters' P_clean."""
    a = slips + 1
    b = items - slips + 1
    choose = math.lgamma(paul_items + 1) - math.lgamma(paul_slips + 1) - math.lgamma(paul_items - paul_slips + 1)
    return math.exp(choose + log_beta(a + paul_slips, b + paul_items - paul_slips) - log_beta(a, b))


def score(name, codes, key, original):
    counts = group_counts(codes, key)
    genuine = counts["genuine"]
    later = counts["later A"]
    paul = counts["Paul"]
    ratio = chance_of_record(genuine["slip"], genuine["items"], paul["slip"], paul["items"]) / chance_of_record(
        later["slip"], later["items"], paul["slip"], paul["items"])
    agreement = kappa(original, codes)
    return {"name": name, "counts": counts, "ratio": ratio, "kappa": agreement,
            "p1": rate(genuine) < 0.10, "p2": rate(later) >= 0.15, "p3": paul["slip"] <= 1,
            "p4": agreement >= 0.5, "p5": ratio > 20}


def met(value):
    if value:
        return "met"
    return "not met"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    key = read_key()
    original = {}
    for identifier, row in key.items():
        original[identifier] = row["original_code"]
    coders = []
    if os.path.isdir(CODERS):
        for filename in sorted(os.listdir(CODERS)):
            if filename.endswith(".txt"):
                coders.append((filename[:-4], read_coder(os.path.join(CODERS, filename), key)))
    if not coders:
        sys.exit(f"No coder files in {CODERS}.")
    results = [score("original (not blind)", original, key, original)]
    for name, codes in coders:
        results.append(score(name, codes, key, original))
    lines = ["# Blind check of the slip coding: results", "",
             "Rules: PREDICTIONS.md (SHA-256 f7b89d0c…0c4e) and AMENDMENTS.md. Generated by blind_check.py.", "",
             "## 1. Slip rates by group (slips / items coded fits, either or slip)", "",
             "| coder | genuine | Group A + 3 Cor | Group B | Paul's core four |", "|---|---|---|---|---|"]
    for result in results:
        cells = []
        for group, label in GROUPS:
            count = result["counts"][group]
            cells.append(f"{count['slip']}/{count['items']} ({100 * rate(count):.0f}%)")
        lines.append(f"| {result['name']} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## 2. Codes by group")
    lines.append("")
    lines.append("| coder | group | fits | either | slip | not |")
    lines.append("|---|---|---|---|---|---|")
    for result in results:
        for group, label in GROUPS:
            count = result["counts"][group]
            lines.append(f"| {result['name']} | {label} | {count['fits']} | {count['either']} | {count['slip']} | "
                         f"{count['not']} |")
    lines.append("")
    lines.append("## 3. Agreement and Paul's record")
    lines.append("")
    lines.append("| coder | kappa with original (slip / not slip) | likelihood ratio for Paul's record (genuine : later) |")
    lines.append("|---|---|---|")
    for result in results:
        lines.append(f"| {result['name']} | {result['kappa']:.2f} | {result['ratio']:.0f} to 1 |")
    if len(coders) >= 2:
        lines.append("")
        lines.append("Kappa between blind coders (slip / not slip):")
        lines.append("")
        for first in range(len(coders)):
            for second in range(first + 1, len(coders)):
                value = kappa(coders[first][1], coders[second][1])
                lines.append(f"- {coders[first][0]} and {coders[second][0]}: {value:.2f}")
    lines.append("")
    lines.append("## 4. Predictions (blind coders only)")
    lines.append("")
    lines.append("| coder | 1. genuine < 10% | 2. Group A + 3 Cor >= 15% | 3. Paul <= 1 slip | 4. kappa >= 0.5 | "
                 "5. ratio > 20 |")
    lines.append("|---|---|---|---|---|---|")
    for result in results[1:]:
        lines.append(f"| {result['name']} | {met(result['p1'])} | {met(result['p2'])} | {met(result['p3'])} | "
                     f"{met(result['p4'])} | {met(result['p5'])} |")
    lines.append("")
    lines.append("## 5. Items where a blind coder and the original differ on slip")
    lines.append("")
    lines.append("| ID | text | original | blind codes |")
    lines.append("|---|---|---|---|")
    for identifier in sorted(key):
        differs = False
        blind = []
        for name, codes in coders:
            blind.append(f"{name}: {codes[identifier]}")
            if (codes[identifier] == "slip") != (original[identifier] == "slip"):
                differs = True
        if differs:
            lines.append(f"| {identifier} | {key[identifier]['text']} | {original[identifier]} | {'; '.join(blind)} |")
    lines.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"Written: {OUTPUT}")


if __name__ == "__main__":
    main()
