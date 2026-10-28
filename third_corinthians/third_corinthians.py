"""
    third_corinthians: 3 Corinthians as a later writer in Paul's name (slips), and 3 Corinthians and Paul's letters to
    Seneca as Latin forgeries (style). Rules in third_corinthians/PREDICTIONS.md (SHA-256 32147012…f277).

    Part A reads third_corinthians/codes.txt and slip_rate/codes.txt.
    Part B reads the Latin texts in third_corinthians/texts/ (prepared from Vouaux 1913, see AMENDMENTS.md) and uses
    rhetoric_across's measures and Clementine Vulgate (python rhetoric_across/fetch_texts.py). If
    rhetoric_across/laodiceans.txt is present, Laodiceans is shown beside them.

    Output: RESULTS.md.

    Usage (from the kit folder):   python -X utf8 third_corinthians/third_corinthians.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(KIT, "rhetoric_across"))
import rhetoric_across as ra

CODES = os.path.join(HERE, "codes.txt")
SLIP_CODES = os.path.join(KIT, "slip_rate", "codes.txt")
TEXTS = [("3 Corinthians", os.path.join(HERE, "texts", "third_corinthians_latin.txt")),
         ("Paul to Seneca", os.path.join(HERE, "texts", "paul_to_seneca_latin.txt")),
         ("Laodiceans", os.path.join(KIT, "rhetoric_across", "laodiceans.txt"))]
OUTPUT = os.path.join(HERE, "RESULTS.md")
GROUP_A = ["Pastorals", "spurious Ignatius", "Clementine letters to James"]
CLOSEST = ["Pastorals", "2 Peter", "Acts of John"]
NEW = "3 Corinthians"


def read_codes(path):
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
            items.append({"text": fields[0], "item": fields[2], "code": fields[3], "strength": fields[4],
                          "reason": fields[5]})
    return items


def tally(items):
    stats = {}
    for item in items:
        if item["code"] == "not":
            continue
        name = item["text"]
        stats.setdefault(name, {"items": 0, "slip": 0, "weak": 0, "strong": 0})
        stats[name]["items"] += 1
        if item["code"] == "slip":
            stats[name]["slip"] += 1
            if item["strength"] == "weak":
                stats[name]["weak"] += 1
            if item["strength"] == "strong":
                stats[name]["strong"] += 1
    return stats


def log_beta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def p_clean(slips, items, n):
    """E[(1 - r)^n] for r ~ Beta(slips + 1, items - slips + 1), as in slip_rate/rates.py."""
    a = slips + 1
    b = items - slips + 1
    return math.exp(log_beta(a, b + n) - log_beta(a, b))


def pooled(stats, members, drop_weak):
    items = 0
    slips = 0
    for name in members:
        items += stats[name]["items"]
        slips += stats[name]["slip"]
        if drop_weak:
            items -= stats[name]["weak"]
            slips -= stats[name]["weak"]
    return items, slips


def part_a(lines):
    own = read_codes(CODES)
    old = read_codes(SLIP_CODES)
    stats = tally(old + own)
    new = stats[NEW]
    paul = stats["core four"]["items"]
    rate = new["slip"] / new["items"]
    lines.append("## 1. Part A: does 3 Corinthians slip?")
    lines.append("")
    medium = new["slip"] - new["weak"] - new["strong"]
    lines.append(f"3 Corinthians: {new['items']} datable items, {new['slip']} slips (strong {new['strong']}, medium "
                 f"{medium}, weak {new['weak']}), slip rate {100 * rate:.0f}%. Without weak slips: "
                 f"{new['slip'] - new['weak']} of {new['items'] - new['weak']} "
                 f"({100 * (new['slip'] - new['weak']) / (new['items'] - new['weak']):.0f}%).")
    lines.append("")
    lines.append("| item | code | strength | reason |")
    lines.append("|---|---|---|---|")
    for item in own:
        if item["code"] != "not":
            lines.append(f"| {item['item']} | {item['code']} | {item['strength']} | {item['reason']} |")
    lines.append("")
    lines.append(f"Paul's core four: {paul} datable items, {stats['core four']['slip']} slips (slip_rate).")
    lines.append("")
    lines.append("| pool | items | slips | pooled rate | P (no slip in Paul's items) |")
    lines.append("|---|---|---|---|---|")
    pools = [("Group A (slip_rate, as registered)", GROUP_A, False),
             ("Group A + 3 Corinthians", GROUP_A + [NEW], False),
             ("Group A + 3 Corinthians, weak slips not counted", GROUP_A + [NEW], True),
             ("Closest in time (slip_rate)", CLOSEST, False),
             ("Closest in time + 3 Corinthians", CLOSEST + [NEW], False)]
    results = {}
    for label, members, drop_weak in pools:
        items, slips = pooled(stats, members, drop_weak)
        value = p_clean(slips, items, paul)
        results[label] = value
        lines.append(f"| {label} | {items} | {slips} | {100 * slips / items:.0f}% | {value:.4f} |")
    lines.append("")
    lines.append(f"3 Corinthians alone (its own rate): P = {p_clean(new['slip'], new['items'], paul):.4f}.")
    lines.append("")
    return {"A1": new["slip"] >= 1, "A2": 0.15 <= rate <= 0.50, "A3": results["Group A + 3 Corinthians"] < 0.05,
            "rate": rate, "p": results["Group A + 3 Corinthians"]}


def read_text(path):
    with open(path, encoding="utf8") as file:
        text = file.read()
    return ra.latin_sentences(text)


def measure(sentences, latin):
    words = []
    for sentence, question in sentences:
        words.extend(sentence)
    size = len(words)
    paul_words = {}
    for code in ra.PAUL:
        flat = []
        for sentence, question in latin[code]:
            flat.extend(sentence)
        paul_words[code] = flat
    all_paul = set()
    for code in ra.PAUL:
        all_paul |= ra.trigrams(paul_words[code])
    own = ra.trigrams(words)
    share = 100.0 * len(own & all_paul) / max(1, len(own))
    baseline = []
    scores = []
    for code in ra.PAUL:
        others = set()
        for other in ra.PAUL:
            if other != code:
                others |= ra.trigrams(paul_words[other])
        for piece in ra.passages(latin[code], size):
            piece_words = []
            for sentence, question in piece:
                piece_words.extend(sentence)
            grams = ra.trigrams(piece_words)
            baseline.append(100.0 * len(grams & others) / max(1, len(grams)))
            scores.append(ra.argument_score(ra.features(piece, "latin")))
    baseline.sort()
    scores.sort()
    score = ra.argument_score(ra.features(sentences, "latin"))
    below = 0
    for value in scores:
        if value < score:
            below += 1
    shared = sorted(own & all_paul)
    return {"size": size, "share": share, "median": baseline[len(baseline) // 2], "highest": baseline[-1],
            "passages": len(baseline), "score": score, "fifth": scores[int(0.05 * (len(scores) - 1))],
            "score_median": scores[len(scores) // 2], "percentile": 100.0 * below / len(scores), "shared": shared}


def part_b(lines):
    latin = ra.latin_letters()
    lines.append("## 2. Part B: Latin style against the Latin Paul")
    lines.append("")
    lines.append("Measures of rhetoric_across Part 2, unchanged. Baselines are passages of Paul of the same length as "
                 "each text.")
    lines.append("")
    lines.append("| text | words | 3-word sequences found in Paul | Paul's passages: median / highest | argument "
                 "score | Paul's passages: 5th percentile / median | text above this share of Paul's passages |")
    lines.append("|---|---|---|---|---|---|---|")
    found = {}
    for name, path in TEXTS:
        if not os.path.exists(path):
            lines.append(f"| {name} | file not found | | | | | |")
            continue
        result = measure(read_text(path), latin)
        found[name] = result
        lines.append(f"| {name} | {result['size']} | {result['share']:.1f}% | {result['median']:.1f}% / "
                     f"{result['highest']:.1f}% ({result['passages']} passages) | {result['score']:.1f} | "
                     f"{result['fifth']:.1f} / {result['score_median']:.1f} | {result['percentile']:.1f}% |")
    lines.append("")
    for name in found:
        lines.append(f"{name}: 3-word sequences found in Paul: " + "; ".join(found[name]["shared"]) + ".")
        lines.append("")
    return found


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    lines = ["# 3 Corinthians and the Latin forgeries of Paul: results", "",
             "Rules: PREDICTIONS.md (SHA-256 32147012…f277) and AMENDMENTS.md. Generated by third_corinthians.py.",
             ""]
    a = part_a(lines)
    b = part_b(lines)
    lines.append("## 3. Predictions")
    lines.append("")
    rows = [("A1. 3 Corinthians has at least one slip", a["A1"], ""),
            ("A2. Its slip rate is between 15% and 50%", a["A2"], f"{100 * a['rate']:.0f}%"),
            ("A3. With 3 Corinthians in Group A, P for Paul's record stays below 0.05", a["A3"], f"P = {a['p']:.4f}")]
    if NEW in b:
        third = b[NEW]
        rows.append(("B1. 3 Corinthians above Paul's median share, not above every passage",
                     third["median"] < third["share"] <= third["highest"],
                     f"{third['share']:.1f}% against median {third['median']:.1f}%, highest {third['highest']:.1f}%"))
        rows.append(("B2. 3 Corinthians' argument score above Paul's 5th percentile", third["score"] > third["fifth"],
                     f"{third['score']:.1f} against {third['fifth']:.1f}"))
    if "Paul to Seneca" in b:
        seneca = b["Paul to Seneca"]
        rows.append(("B3. Paul to Seneca below Paul's median share and below his 5th percentile on argument",
                     seneca["share"] < seneca["median"] and seneca["score"] < seneca["fifth"],
                     f"share {seneca['share']:.1f}% (median {seneca['median']:.1f}%); argument {seneca['score']:.1f} "
                     f"(5th percentile {seneca['fifth']:.1f})"))
    lines.append("| prediction | met? | detail |")
    lines.append("|---|---|---|")
    for text, met, detail in rows:
        word = "not met"
        if met:
            word = "met"
        lines.append(f"| {text} | {word} | {detail} |")
    lines.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"Written: {OUTPUT}")


if __name__ == "__main__":
    main()
