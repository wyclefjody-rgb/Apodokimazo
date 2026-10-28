"""
    real_letters: do genuine letters "slip" under the slip test? Genuine controls for slip_rate and
    third_corinthians. Rules in real_letters/PREDICTIONS.md (SHA-256 4987661a…f143).

    Reads real_letters/codes.txt (hand-coded), slip_rate/codes.txt and third_corinthians/codes.txt (the forgeries and
    Paul), and counts the words of the sampled letters in Perseus canonical-latinLit
    (python real_letters/fetch_texts.py adds them).

    Output: RESULTS.md.

    Usage (from the kit folder):   python -X utf8 real_letters/real_letters.py
"""
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
LATIN = os.path.join(KIT, "canonical-latinLit", "data")
CODES = os.path.join(HERE, "codes.txt")
SLIP_CODES = os.path.join(KIT, "slip_rate", "codes.txt")
THIRD_CODES = os.path.join(KIT, "third_corinthians", "codes.txt")
OUTPUT = os.path.join(HERE, "RESULTS.md")
NS = "{http://www.tei-c.org/ns/1.0}"
SAMPLES = [("Pliny", os.path.join("phi1318", "phi001", "phi1318.phi001.perseus-lat1.xml"), "10",
            list(range(1, 61)) + [96, 97]),
           ("Cicero", os.path.join("phi0474", "phi057", "phi0474.phi057.perseus-lat2.xml"), "1", list(range(1, 21))),
           ("Seneca", os.path.join("phi1017", "phi015", "phi1017.phi015.perseus-lat2.xml"), None, list(range(1, 31)))]
FORGERIES = ["Pastorals", "spurious Ignatius", "Clementine letters to James", "3 Corinthians"]
ALL_LATER = FORGERIES + ["2 Peter", "Acts of John", "Acts of Thomas", "Acts of Barnabas"]
CLOSEST = ["Pastorals", "2 Peter", "Acts of John", "3 Corinthians"]
DROP = (NS + "note", NS + "bibl", NS + "label", NS + "head")
PAUL_ITEMS = 16


def read_codes(path, first_field):
    if not os.path.exists(path):
        sys.exit(f"Missing {path}.")
    items = []
    with open(path, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = []
            for part in line.split("|"):
                fields.append(part.strip())
            if len(fields) < 6:
                sys.exit(f"Short line in {path}: {line[:80]}")
            items.append({"name": fields[first_field], "where": fields[1], "item": fields[2], "code": fields[3],
                          "strength": fields[4], "reason": fields[5]})
    return items


def tally(items):
    stats = {}
    for item in items:
        stats.setdefault(item["name"], {"items": 0, "slip": 0, "fits": 0, "either": 0, "not": 0})
        stats[item["name"]][item["code"]] += 1
        if item["code"] != "not":
            stats[item["name"]]["items"] += 1
    return stats


def letter_number(value):
    digits = re.sub(r"[a-z]$", "", value or "")
    if digits.isdigit():
        return int(digits)
    return -1


def remove_dropped(element):
    for parent in list(element.iter()):
        for child in list(parent):
            if child.tag in DROP:
                tail = child.tail
                parent.remove(child)
                if tail:
                    parent.text = (parent.text or "") + " " + tail


def sample_words(path, book, letters):
    full = os.path.join(LATIN, path)
    if not os.path.exists(full):
        sys.exit(f"Missing {full}. Run: python real_letters/fetch_texts.py")
    root = ET.parse(full).getroot()
    count = 0
    for division in root.iter(NS + "div"):
        if division.get("subtype") != "book":
            continue
        if book is not None and division.get("n") != book:
            continue
        for letter in division.iter(NS + "div"):
            if letter.get("subtype") != "letter" or letter_number(letter.get("n")) not in letters:
                continue
            remove_dropped(letter)
            for token in " ".join(letter.itertext()).split():
                if re.search(r"[A-Za-z]", token):
                    count += 1
    return count


def log_beta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def p_clean(slips, items, n):
    """E[(1 - r)^n] for r ~ Beta(slips + 1, items - slips + 1), as in slip_rate/rates.py."""
    a = slips + 1
    b = items - slips + 1
    return math.exp(log_beta(a, b + n) - log_beta(a, b))


def beta_cdf(x, a, b, steps=20000):
    """Regularized incomplete beta by the midpoint rule (enough for intervals to three decimals)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    total = 0.0
    width = x / steps
    for step in range(steps):
        t = (step + 0.5) * width
        total += math.exp((a - 1) * math.log(t) + (b - 1) * math.log(1 - t))
    return total * width / math.exp(log_beta(a, b))


def beta_quantile(q, a, b):
    low = 0.0
    high = 1.0
    for round_number in range(40):
        middle = (low + high) / 2
        if beta_cdf(middle, a, b, 4000) < q:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def interval(slips, items):
    a = slips + 1
    b = items - slips + 1
    return beta_quantile(0.025, a, b), beta_quantile(0.975, a, b)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    genuine = read_codes(CODES, 0)
    stats = tally(genuine)
    others = tally(read_codes(SLIP_CODES, 0) + read_codes(THIRD_CODES, 0))
    lines = ["# Do genuine letters slip? Results", "",
             "Rules: PREDICTIONS.md (SHA-256 4987661a…f143) and AMENDMENTS.md. Generated by real_letters.py from "
             "codes.txt.", "",
             "## 1. Genuine letters", "",
             "| collection | words in the sample | datable items | fits | either | slips | slip rate (95% interval) | "
             "datable items per 1,000 words |",
             "|---|---|---|---|---|---|---|---|"]
    density = {}
    pooled_items = 0
    pooled_slips = 0
    each_ok = True
    for name, path, book, letters in SAMPLES:
        words = sample_words(path, book, letters)
        s = stats.get(name, {"items": 0, "slip": 0, "fits": 0, "either": 0})
        low, high = interval(s["slip"], s["items"])
        rate = s["slip"] / max(1, s["items"])
        if rate >= 0.05:
            each_ok = False
        density[name] = 1000.0 * s["items"] / max(1, words)
        pooled_items += s["items"]
        pooled_slips += s["slip"]
        lines.append(f"| {name} | {words:,} | {s['items']} | {s['fits']} | {s['either']} | {s['slip']} | "
                     f"{100 * rate:.0f}% ({100 * low:.1f}-{100 * high:.1f}%) | {density[name]:.2f} |")
    g_low, g_high = interval(pooled_slips, pooled_items)
    lines.append(f"| **all genuine** | | {pooled_items} | | | {pooled_slips} | "
                 f"{100 * pooled_slips / pooled_items:.0f}% ({100 * g_low:.1f}-{100 * g_high:.1f}%) | |")
    lines.append("")
    forged_items = 0
    forged_slips = 0
    lines.append("## 2. Known later writings (slip_rate Group A and 3 Corinthians)")
    lines.append("")
    lines.append("| text | datable items | slips |")
    lines.append("|---|---|---|")
    for name in FORGERIES:
        forged_items += others[name]["items"]
        forged_slips += others[name]["slip"]
        lines.append(f"| {name} | {others[name]['items']} | {others[name]['slip']} |")
    f_low, f_high = interval(forged_slips, forged_items)
    lines.append(f"| **all** | {forged_items} | {forged_slips} ({100 * forged_slips / forged_items:.0f}%, 95% interval "
                 f"{100 * f_low:.1f}-{100 * f_high:.1f}%) |")
    lines.append("")
    paul = others["core four"]
    if paul["items"] != PAUL_ITEMS:
        sys.exit(f"Expected {PAUL_ITEMS} items for the core four in slip_rate/codes.txt, found {paul['items']}.")
    clean_genuine = p_clean(pooled_slips, pooled_items, PAUL_ITEMS)
    clean_forged = p_clean(forged_slips, forged_items, PAUL_ITEMS)
    ratio = clean_genuine / clean_forged
    lines.append("## 3. Paul's record weighed both ways")
    lines.append("")
    lines.append(f"Paul's core four: {paul['items']} datable items, {paul['slip']} slips (slip_rate).")
    lines.append("")
    lines.append("| if the letters were written by | chance of 0 slips in 16 items |")
    lines.append("|---|---|")
    lines.append(f"| a writer like the genuine letter-writers | {clean_genuine:.3f} |")
    lines.append(f"| a writer like the known later writers | {clean_forged:.4f} |")
    lines.append(f"| **likelihood ratio (genuine : later)** | **{ratio:.0f} to 1** |")
    lines.append("")
    lines.append("Exploratory (AMENDMENTS.md 1): the same ratio against other sets of later writings.")
    lines.append("")
    lines.append("| later writings | items | slips | chance of 0 in 16 | likelihood ratio |")
    lines.append("|---|---|---|---|---|")
    for label, members in [("Group A and 3 Corinthians (registered)", FORGERIES),
                           ("all eight later writings (Groups A and B, 3 Corinthians)", ALL_LATER),
                           ("closest in time (Pastorals, 2 Peter, Acts of John, 3 Corinthians)", CLOSEST)]:
        items = 0
        slips = 0
        for name in members:
            items += others[name]["items"]
            slips += others[name]["slip"]
        value = p_clean(slips, items, PAUL_ITEMS)
        lines.append(f"| {label} | {items} | {slips} | {value:.4f} | {clean_genuine / value:.0f} to 1 |")
    lines.append("")
    lines.append("## 4. Predictions")
    lines.append("")
    rows = [("1. Each collection's slip rate below 5%", each_ok, ""),
            ("2. Pooled genuine rate below 5%, intervals not overlapping the forgeries'",
             pooled_slips / pooled_items < 0.05 and g_high < f_low,
             f"genuine {100 * g_low:.1f}-{100 * g_high:.1f}%, later {100 * f_low:.1f}-{100 * f_high:.1f}%"),
            ("3. Likelihood ratio for Paul's record above 20", ratio > 20, f"{ratio:.0f} to 1"),
            ("4. Seneca has fewer datable items per 1,000 words than Pliny and Cicero",
             density["Seneca"] < density["Pliny"] and density["Seneca"] < density["Cicero"],
             f"Seneca {density['Seneca']:.2f}, Pliny {density['Pliny']:.2f}, Cicero {density['Cicero']:.2f}")]
    lines.append("| prediction | met? | detail |")
    lines.append("|---|---|---|")
    for text, met, detail in rows:
        word = "not met"
        if met:
            word = "met"
        lines.append(f"| {text} | {word} | {detail} |")
    lines.append("")
    lines.append("## 5. Every genuine item that is not \"not\"")
    lines.append("")
    lines.append("| collection | letter | item | code | evidence |")
    lines.append("|---|---|---|---|---|")
    for item in genuine:
        if item["code"] != "not":
            lines.append(f"| {item['name']} | {item['where']} | {item['item']} | {item['code']} | {item['reason']} |")
    lines.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"Written: {OUTPUT}")


if __name__ == "__main__":
    main()
