"""
    One writer or a school? (one_hand/PREDICTIONS.md)

    Each letter collection is cut into units (consecutive letters joined to at least 1,000 words) and blocks of
    500 words. A unit's outsider ratio R compares its first two blocks with the rest of its collection:

      R = mean distance(unit's first two blocks, blocks of the other units)
          / mean distance(blocks of the other units that belong to different units)

    Distances are Cosine Delta on the 100 most frequent function words, z-scored over every block of the study.
    The threshold for "stands apart" is the 95th percentile of R in five single-author letter collections.

    Needs: sblgnt/ and First1KGreek/ (setup_data.py; the authors used here are already in steps 1-12).
    Output: RESULTS.md.

    Usage (from the kit folder):   python -X utf8 one_hand/one_hand.py
"""
import os
import sys
from collections import Counter
from glob import glob

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(KIT, "paul_lineup"))
sys.path.insert(0, os.path.join(KIT, "advanced"))
from words import function_form, keep_accents
import extract

extract.norm = keep_accents

SBLGNT = os.path.join(KIT, "sblgnt")
FIRST1K = os.path.join(KIT, "First1KGreek", "data")
FUNCTION_WORDS = os.path.join(KIT, "paul_lineup", "features", "function_words.txt")
OUTPUT = os.path.join(HERE, "RESULTS.md")

BLOCK = 500
MFW_COUNT = 100
PERCENTILE = 95
MIN_UNITS = 3
VERSIONS = [
    {"name": "Version 1 (PREDICTIONS.md)", "unit_min": 1000, "first_blocks": 2, "libanius": 20000, "local": False},
    {"name": "Version 2 (AMENDMENTS.md 2)", "unit_min": 2000, "first_blocks": 4, "libanius": 40000, "local": True},
]

PAUL = ["Ro", "1Co", "2Co", "Ga", "Php", "1Th", "Phm"]
SINGLE_AUTHOR = ["Ignatius", "Chion", "Themistocles", "Alciphron", "Libanius"]
MULTI_AUTHOR = ["Diogenes", "Crates", "Socratic letters"]
ALSO = ["Phalaris"]
FIRST1K_TEXTS = {
    "Ignatius": [("tlg1443", "tlg001", "epistle", None)],
    "Ignatius, spurious letters": [("tlg1443", "tlg002", "epistle", ["13", "1", "4", "5", "9", "10"])],
    "1 Clement": [("tlg1271", "tlg001", None, None)],
    "Chion": [("tlg0041", "tlg001", "epistle", None)],
    "Themistocles": [("tlg0055", "tlg001", "epistle", None)],
    "Alciphron": [("tlg0640", "tlg001", "section", None)],
    "Libanius": [("tlg2200", "tlg001", "letter", None)],
    "Diogenes": [("tlg1325", "tlg001", "epistle", None)],
    "Crates": [("tlg0623", "tlg001", "epistle", None)],
    "Socratic letters": [("tlg0636", "tlg001", "epistle", None), ("tlg0637", "tlg001", "epistle", None)],
    "Phalaris": [("tlg0053", "tlg001", "epistle", None)],
}
SPURIOUS_NAMES = {"13": "Mary to Ignatius", "1": "to Mary", "4": "Tarsians", "5": "Philippians", "9": "Antiochenes",
                  "10": "Hero"}


def sblgnt_letter(book):
    paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
    if not paths:
        sys.exit(f"No MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
    words = []
    with open(paths[0], encoding="utf8") as file:
        for line in file:
            word = keep_accents(line.split()[4])
            if word:
                words.append(function_form(word))
    return words


def first1k_letters(author, work, level, pick):
    paths = glob(os.path.join(FIRST1K, author, work, f"{author}.{work}.1st1K-grc*.xml"))
    if not paths:
        sys.exit(f"No First1KGreek file for {author}.{work} in '{FIRST1K}'. Run setup_data.py first.")
    if level is None:
        parts = [("1", extract.load(paths[0]))]
    else:
        parts = extract.parts(paths[0], level)
    letters = []
    for number, raw in parts:
        if pick is not None and number not in pick:
            continue
        words = []
        for word in raw:
            words.append(function_form(word))
        if words:
            letters.append((number, words))
    if pick is not None:
        ordered = []
        for number in pick:
            for letter in letters:
                if letter[0] == number:
                    ordered.append(letter)
        letters = ordered
    return letters


def collection(name):
    letters = []
    for author, work, level, pick in FIRST1K_TEXTS[name]:
        letters.extend(first1k_letters(author, work, level, pick))
    if name == "Ignatius, spurious letters":
        named = []
        for number, words in letters:
            named.append((SPURIOUS_NAMES[number], words))
        letters = named
    return letters


def first_words(letters, limit):
    kept = []
    total = 0
    for letter in letters:
        if total >= limit:
            break
        kept.append(letter)
        total += len(letter[1])
    return kept


def units_of(letters, unit_min, prefix=""):
    units = []
    label = []
    words = []
    for number, letter_words in letters:
        label.append(str(number))
        words.extend(letter_words)
        if len(words) >= unit_min:
            units.append((prefix + "+".join(label), words))
            label = []
            words = []
    if words:
        if units:
            last_label, last_words = units[-1]
            units[-1] = (last_label + "+" + "+".join(label), last_words + words)
        else:
            units.append((prefix + "+".join(label) + " (too short)", words))
    return units


def blocks_of(words):
    blocks = []
    for start in range(0, len(words) - BLOCK + 1, BLOCK):
        blocks.append(words[start:start + BLOCK])
    return blocks


def read_function_words():
    if not os.path.exists(FUNCTION_WORDS):
        sys.exit(f"'{FUNCTION_WORDS}' not found. Run  python paul_lineup/make_function_words.py  first.")
    forms = []
    with open(FUNCTION_WORDS, encoding="utf8") as file:
        for line in file:
            if line.startswith("#") or not line.strip():
                continue
            forms.append(line.split("|")[0].strip())
    return forms


def choose_vocabulary(texts, candidates):
    weights = Counter()
    for name, letters in texts.items():
        counts = Counter()
        size = 0
        for number, words in letters:
            counts.update(words)
            size += len(words)
        for form in candidates:
            weights[form] += counts[form] / size
    chosen = []
    for form, weight in weights.most_common(MFW_COUNT):
        chosen.append(form)
    return chosen


def rates(block, vocabulary):
    counts = Counter(block)
    row = []
    for form in vocabulary:
        row.append(counts[form] / len(block))
    return row


class Space:
    """The study-wide scale (version 1): mean and spread of every block of the study."""

    def __init__(self, texts, vocabulary):
        self.vocabulary = vocabulary
        rows = []
        for name, letters in texts.items():
            for number, words in letters:
                for block in blocks_of(words):
                    rows.append(rates(block, vocabulary))
        rows = np.array(rows)
        self.centre = rows.mean(axis=0)
        self.spread = rows.std(axis=0) + 1e-9

    def raw(self, words):
        rows = []
        for block in blocks_of(words):
            rows.append(rates(block, self.vocabulary))
        return np.array(rows)


def outsider_ratios(space, units, settings, targets=None, windows=False):
    """R for every unit named in targets (all units if None). With windows, R for every window of first_blocks
    blocks. With settings["local"], z-scores use the blocks of these units only (version 2)."""
    first_blocks = settings["first_blocks"]
    raw = []
    owners = []
    for index in range(len(units)):
        rows = space.raw(units[index][1])
        raw.append(rows)
        for row in rows:
            owners.append(index)
    owners = np.array(owners)
    if settings["local"]:
        stacked = np.vstack(raw)
        centre = stacked.mean(axis=0)
        spread = stacked.std(axis=0) + 1e-9
    else:
        centre = space.centre
        spread = space.spread
    profiles = []
    for rows in raw:
        z = (rows - centre) / spread
        profiles.append(z / (np.linalg.norm(z, axis=1, keepdims=True) + 1e-12))
    everything = np.vstack(profiles)
    results = []
    for index in range(len(units)):
        label = units[index][0]
        if targets is not None and label not in targets:
            continue
        if len(units) < MIN_UNITS:
            results.append((label, None))
            continue
        others = everything[owners != index]
        other_owners = owners[owners != index]
        similarity = others @ others.T
        different = other_owners[:, None] != other_owners[None, :]
        baseline = (1 - similarity)[different].mean()
        own = profiles[index]
        if len(own) < first_blocks:
            results.append((label, None))
            continue
        starts = [0]
        if windows:
            starts = list(range(0, len(own) - first_blocks + 1))
        values = []
        for start in starts:
            chosen = own[start:start + first_blocks]
            values.append(float((1 - chosen @ others.T).mean() / baseline))
        results.append((label, values if windows else values[0]))
    return results


def report(texts, space, settings):
    unit_min = settings["unit_min"]
    lines = [f"# {settings['name']}", "",
             f"Units of at least {unit_min:,} words; R uses each unit's first {settings['first_blocks']} blocks; "
             f"z-scores over {'the collection being tested' if settings['local'] else 'every block of the study'}; "
             f"Libanius up to {settings['libanius']:,} words.", ""]
    texts = dict(texts)
    texts["Libanius"] = first_words(texts["Libanius"], settings["libanius"])

    lines.append("### 1. Calibration: single-author letter collections")
    lines.append("")
    lines.append("| collection | units | words | R of each unit |")
    lines.append("|---|---|---|---|")
    calibration = []
    calibration_rows = []
    for name in SINGLE_AUTHOR:
        units = units_of(texts[name], unit_min)
        ratios = outsider_ratios(space, units, settings)
        shown = []
        for label, value in ratios:
            if value is not None:
                calibration.append(value)
                shown.append(f"{label}: {value:.3f}")
        size = 0
        for label, words in units:
            size += len(words)
        calibration_rows.append((name, units, size, shown))
    threshold = float(np.percentile(calibration, PERCENTILE))
    for name, units, size, shown in calibration_rows:
        shown_text = "; ".join(shown) if shown else f"fewer than {MIN_UNITS} units: not used"
        lines.append(f"| {name} | {len(units)} | {size:,} | {shown_text} |")
    flagged = 0
    for value in calibration:
        if value > threshold:
            flagged += 1
    lines.append("")
    lines.append(f"Threshold (the {PERCENTILE}th percentile of {len(calibration)} single-author units): "
                 f"**R = {threshold:.3f}**. Single-author units above it: {flagged} of {len(calibration)}.")
    lines.append("")

    def mark(value):
        if value is None:
            return "too short"
        return f"{value:.3f}{' **flagged**' if value > threshold else ''}"

    paul_units = units_of(texts["Paul"], unit_min)
    lines.append("### 2. Sensitivity: known second hands added to a collection")
    lines.append("")
    lines.append("| added to | added texts | unit | R | |")
    lines.append("|---|---|---|---|---|")
    sensitivity = [
        ("Paul's seven letters", "the Pastorals", paul_units, units_of(texts["Pastorals"], unit_min)),
        ("Paul's seven letters", "Hebrews", paul_units, units_of(texts["Hebrews"], unit_min)),
        ("Paul's seven letters", "1 Clement", paul_units, units_of(texts["1 Clement"], unit_min, "1 Clement ")),
        ("Paul's seven letters", "Ignatius' seven letters", paul_units, units_of(texts["Ignatius"], unit_min, "Ignatius ")),
        ("Ignatius' seven letters", "the six spurious Ignatian letters", units_of(texts["Ignatius"], unit_min),
         units_of(texts["Ignatius, spurious letters"], unit_min)),
    ]
    passes = {}
    for host, added_name, host_units, added_units in sensitivity:
        targets = set()
        for label, words in added_units:
            targets.add(label)
        ratios = outsider_ratios(space, host_units + added_units, settings, targets)
        hits = 0
        for label, value in ratios:
            if value is not None and value > threshold:
                hits += 1
            lines.append(f"| {host} | {added_name} | {label} | {mark(value)} | |")
        passes[added_name] = (hits, len(ratios))
    lines.append("")
    rules = [("the Pastorals", "all"), ("Hebrews", "all"), ("1 Clement", "all"), ("Ignatius' seven letters", "half"),
             ("the six spurious Ignatian letters", "half")]
    works = True
    for name, need in rules:
        hits, total = passes[name]
        ok = hits == total if need == "all" else hits * 2 >= total
        if not ok:
            works = False
        lines.append(f"- {name}: {hits} of {total} units flagged (needed: {need}) - **{'pass' if ok else 'fail'}**")
    lines.append("")
    lines.append(f"**The method works (PREDICTIONS.md section 4): {'yes' if works else 'no'}.**")
    lines.append("")

    lines.append("### 3. The test: Paul's seven letters")
    lines.append("")
    lines.append("| unit | words | R | |")
    lines.append("|---|---|---|---|")
    paul_flags = 0
    for label, value in outsider_ratios(space, paul_units, settings):
        size = 0
        for unit_label, words in paul_units:
            if unit_label == label:
                size = len(words)
        if value is not None and value > threshold:
            paul_flags += 1
        lines.append(f"| {label} | {size:,} | {mark(value)} | |")
    lines.append("")
    verdict = "several hands (two or more units flagged)" if paul_flags >= 2 else "one hand (at most one unit flagged)"
    lines.append(f"Units flagged: **{paul_flags} of {len(paul_units)}**. By the rule set in advance: **{verdict}**"
                 f"{'' if works else ', but the method failed its sensitivity tests, so no conclusion is drawn'}.")
    lines.append("")
    lines.append(f"Robustness (not decisive): R for every window of {settings['first_blocks']} consecutive blocks "
                 "in each unit")
    lines.append("")
    lines.append("| letter | windows | lowest | median | highest | windows above threshold |")
    lines.append("|---|---|---|---|---|---|")
    for label, values in outsider_ratios(space, paul_units, settings, windows=True):
        if values is None:
            continue
        above = 0
        for value in values:
            if value > threshold:
                above += 1
        lines.append(f"| {label} | {len(values)} | {min(values):.3f} | {float(np.median(values)):.3f} | "
                     f"{max(values):.3f} | {above} |")
    lines.append("")

    lines.append("### 4. Collections held to have several authors (descriptive)")
    lines.append("")
    lines.append("| collection | units | flagged | R of each unit |")
    lines.append("|---|---|---|---|")
    for name in MULTI_AUTHOR + ALSO:
        units = units_of(texts[name], unit_min)
        ratios = outsider_ratios(space, units, settings)
        hits = 0
        shown = []
        for label, value in ratios:
            if value is not None and value > threshold:
                hits += 1
            shown.append(f"{label}: {mark(value)}")
        lines.append(f"| {name} | {len(units)} | {hits} | {'; '.join(shown)} |")
    lines.append("")
    lines.append("Phalaris is reported alongside; its authorship is debated.")
    lines.append("")

    lines.append("### 5. Disputed letters among Paul's (reported, not decisive)")
    lines.append("")
    lines.append("| unit | R | |")
    lines.append("|---|---|---|")
    disputed = [("Eph", sblgnt_letter("Eph")), ("Col", sblgnt_letter("Col"))]
    disputed_units = []
    for label, words in disputed:
        disputed_units.append((label, words))
    ratios = outsider_ratios(space, paul_units + disputed_units, settings, {"Eph", "Col"})
    for label, value in ratios:
        lines.append(f"| {label} | {mark(value)} | |")
    lines.append("")
    lines.append(f"2 Thessalonians ({len(sblgnt_letter('2Th'))} words) is under {unit_min:,} words and is not tested.")
    lines.append("")

    return lines




def main():
    sys.stdout.reconfigure(encoding="utf-8")
    texts = {}
    paul = []
    for book in PAUL:
        paul.append((book, sblgnt_letter(book)))
    texts["Paul"] = paul
    pastorals = []
    for book in ["1Ti", "2Ti", "Tit"]:
        pastorals.append((book, sblgnt_letter(book)))
    texts["Pastorals"] = pastorals
    texts["Hebrews"] = [("Heb", sblgnt_letter("Heb"))]
    texts["Ephesians and Colossians"] = [("Eph", sblgnt_letter("Eph")), ("Col", sblgnt_letter("Col"))]
    for name in FIRST1K_TEXTS:
        texts[name] = collection(name)
    scale_texts = dict(texts)
    scale_texts["Libanius"] = first_words(texts["Libanius"], VERSIONS[0]["libanius"])
    vocabulary = choose_vocabulary(scale_texts, read_function_words())
    space = Space(scale_texts, vocabulary)
    lines = ["# One writer or a school? Results", "",
             "Rules: PREDICTIONS.md (SHA-256 6e586157…2c0e48) and AMENDMENTS.md. Generated by one_hand.py. "
             f"Blocks of {BLOCK} words; {MFW_COUNT} function words. Version 1 is the method set in advance; version 2 "
             "is the one set out in AMENDMENTS.md 2 after version 1 failed its sensitivity tests.", ""]
    for settings in VERSIONS:
        lines.extend(report(texts, space, settings))
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
