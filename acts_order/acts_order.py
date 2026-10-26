"""
    Which came first, Acts or Paul's letters? Part A of acts_order/PREDICTIONS.md.

    Leakage tests: a writer's characteristic words (lemmas) are counted in passages where another writer may have
    borrowed from him, and compared with random passages of the same sizes from the rest of the borrower's text.

      C   Markan words in Luke's Markan blocks vs his other blocks (positive control)
      D1  Pauline words in Paul's speeches in Acts vs the other speeches in Acts
      D2  Lukan words in the letters' autobiographical passages vs the rest of the letters
      G   Lukan words in the letters' non-Acts narrative passages vs the rest of the letters (genre control)

    Part A2: lemma three-word sequences shared by Acts and the letters (and, as control, by Luke and the letters)
    and found in no reference book.

    Output: RESULTS.md.

    Usage (from the kit folder):   python -X utf8 acts_order/acts_order.py
"""
import os
import random
import re
import sys
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
SBLGNT = os.path.join(KIT, "sblgnt")
OUTPUT = os.path.join(HERE, "RESULTS.md")

SEED = 0
DRAWS = 10000
PIECE = 300
MIN_COUNT = 5
RATIO = 4
SENSITIVITY = [2, 8]
SMOOTHING = 0.5

PAUL = ["Ro", "1Co", "2Co", "Ga", "Php", "1Th", "Phm"]
REFERENCE = ["Mt", "Mk", "Jn", "Heb", "Jas", "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jud", "Re"]
MARK_REFERENCE = ["Jn", "Heb", "Jas", "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jud", "Re"]

PAUL_SPEECHES = "Ac 13:16-41; Ac 14:15-17; Ac 17:22-31; Ac 20:18-35; Ac 22:1-21; Ac 24:10-21; Ac 26:2-23; " \
                "Ac 28:17-20; Ac 28:25-28"
OTHER_SPEECHES = "Ac 1:16-22; Ac 2:14-40; Ac 3:12-26; Ac 4:8-12; Ac 5:35-39; Ac 7:2-53; Ac 10:34-43; Ac 11:4-17; " \
                 "Ac 15:7-11; Ac 15:13-21; Ac 19:25-27; Ac 19:35-40; Ac 24:2-8; Ac 25:14-21; Ac 25:24-27"
AUTOBIOGRAPHY = "Ga 1:11-2:14; 2Co 11:22-33; 1Th 2:1-3:6; Php 3:4-6; Ro 15:14-33; 1Co 15:8-10; 1Co 16:1-12"
GENRE_CONTROL = "Ro 4:1-25; Ro 9:6-18; 1Co 10:1-11; Ga 4:21-31"
LUKE_FROM_MARK = "Lk 4:31-6:19; Lk 8:4-9:50; Lk 18:15-21:38"
LUKE_NOT_MARK = "Lk 1:5-2:52; Lk 6:20-8:3; Lk 9:51-18:14"
ACTS_WITHOUT_PAUL = "Ac 1:1-8:40; Ac 9:32-11:24; Ac 12:1-24"

RANGE = re.compile(r"^(\S+) (\d+):(\d+)-(?:(\d+):)?(\d+)$")


def load(book):
    paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
    if not paths:
        sys.exit(f"No MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
    tokens = []
    with open(paths[0], encoding="utf8") as file:
        for line in file:
            columns = line.split()
            tokens.append((int(columns[0][2:4]), int(columns[0][4:6]), columns[6], columns[1]))
    return tokens


BOOKS = {}


def book(code):
    if code not in BOOKS:
        BOOKS[code] = load(code)
    return BOOKS[code]


def ranges(spec):
    found = []
    for part in spec.split(";"):
        match = RANGE.match(part.strip())
        if not match:
            sys.exit(f"Cannot read passage '{part}'")
        code = match.group(1)
        start = (int(match.group(2)), int(match.group(3)))
        end_chapter = int(match.group(4)) if match.group(4) else start[0]
        found.append((code, start, (end_chapter, int(match.group(5)))))
    return found


def inside(token, start, end):
    place = (token[0], token[1])
    return start <= place <= end


def passages(spec):
    """Each range of spec as its own list of tokens."""
    segments = []
    for code, start, end in ranges(spec):
        segment = []
        for token in book(code):
            if inside(token, start, end):
                segment.append(token)
        if not segment:
            sys.exit(f"Passage {code} {start}-{end} is empty")
        segments.append(segment)
    return segments


def books_without(codes, spec):
    """Whole books, cut into the runs of tokens that lie outside every range of spec."""
    excluded = ranges(spec) if spec else []
    segments = []
    for code in codes:
        run = []
        for token in book(code):
            skip = False
            for other, start, end in excluded:
                if other == code and inside(token, start, end):
                    skip = True
            if skip:
                if run:
                    segments.append(run)
                run = []
            else:
                run.append(token)
        if run:
            segments.append(run)
    return segments


def counts(segments):
    found = {}
    total = 0
    for segment in segments:
        for token in segment:
            lemma = token[2]
            found[lemma] = found.get(lemma, 0) + 1
            total += 1
    return found, total


def characteristic(base, reference, ratio):
    base_counts, base_total = counts(base)
    reference_counts, reference_total = counts(reference)
    words = set()
    for lemma, number in base_counts.items():
        if number < MIN_COUNT or lemma[0].isupper():
            continue
        base_rate = number / base_total
        reference_rate = (reference_counts.get(lemma, 0) + SMOOTHING) / reference_total
        if base_rate >= ratio * reference_rate:
            words.add(lemma)
    return words


def pieces(segments):
    cut = []
    for segment in segments:
        for start in range(0, len(segment), PIECE):
            cut.append(segment[start:start + PIECE])
    return cut


def share(segments, words):
    hits = 0
    total = 0
    for segment in segments:
        for token in segment:
            total += 1
            if token[2] in words:
                hits += 1
    return hits, total


def permutation(target, pool, words):
    """One-sided p: random passages from pool, matched to target's pieces, with a share at least target's."""
    rng = random.Random(SEED)
    cumulative = []
    for segment in pool:
        running = [0]
        for token in segment:
            running.append(running[-1] + (1 if token[2] in words else 0))
        cumulative.append(running)
    lengths = []
    for piece in pieces(target):
        lengths.append(len(piece))
    starts = {}
    for length in set(lengths):
        options = []
        total = 0
        for index in range(len(pool)):
            possible = len(pool[index]) - length + 1
            if possible > 0:
                total += possible
                options.append((total, index))
        if not options:
            sys.exit(f"No comparison passage is {length} words long")
        starts[length] = (total, options)
    hits, size = share(target, words)
    observed = hits / size
    higher = 0
    draws = []
    for draw in range(DRAWS):
        drawn = 0
        for length in lengths:
            total, options = starts[length]
            pick = rng.randrange(total)
            before = 0
            for limit, index in options:
                if pick < limit:
                    offset = pick - before
                    drawn += cumulative[index][offset + length] - cumulative[index][offset]
                    break
                before = limit
        rate = drawn / size
        draws.append(rate)
        if rate >= observed:
            higher += 1
    mean = sum(draws) / len(draws)
    return observed, mean, (higher + 1) / (DRAWS + 1), hits, size


def hit_words(segments, words):
    found = {}
    for segment in segments:
        for token in segment:
            if token[2] in words:
                found[token[2]] = found.get(token[2], 0) + 1
    ordered = []
    for lemma, number in found.items():
        ordered.append((-number, lemma))
    ordered.sort()
    shown = []
    for number, lemma in ordered:
        shown.append(f"{lemma} {-number}")
    return ", ".join(shown)


def trigrams(segments, label):
    """Three-lemma sequences with at least one noun, verb or adjective, each with the places it starts
    (prefixed by label when label is given)."""
    found = {}
    for segment in segments:
        for i in range(len(segment) - 2):
            three = segment[i:i + 3]
            content = False
            for token in three:
                if token[3][0] in "NVA":
                    content = True
            if not content:
                continue
            key = (three[0][2], three[1][2], three[2][2])
            place = f"{three[0][0]}:{three[0][1]}"
            if label:
                place = f"{label} {place}"
            found.setdefault(key, []).append(place)
    return found


def letters_trigrams():
    found = {}
    for code in PAUL:
        for key, places in trigrams([book(code)], code).items():
            found.setdefault(key, []).extend(places)
    return found


def shared_phrases(code, letters, reference_set):
    text = trigrams([book(code)], "")
    shared = []
    for key in text:
        if key in letters and key not in reference_set:
            shared.append((key, text[key], letters[key]))
    shared.sort()
    return shared


def without_speeches(spec):
    speeches = ranges(PAUL_SPEECHES + "; " + OTHER_SPEECHES)
    kept = []
    for segment in passages(spec):
        for token in segment:
            skip = False
            for code, start, end in speeches:
                if code == "Ac" and inside(token, start, end):
                    skip = True
            if not skip:
                kept.append(token)
    return [kept]


def exploratory(reference, pauline_base, lukan_base):
    """Checks added after the first run (WRITEUP.md); not part of the pre-registered tests."""
    lines = ["## Exploratory checks (added after the first run; not pre-registered)", ""]
    pauline = characteristic(pauline_base, reference, RATIO)
    lukan = characteristic(lukan_base, reference, RATIO)
    no_address = set(pauline)
    no_address.discard("ἀνήρ")
    pauline_only = set()
    for lemma in no_address:
        if lemma not in lukan:
            pauline_only.add(lemma)
    paul = passages(PAUL_SPEECHES)
    others = passages(OTHER_SPEECHES)
    peter = passages("Ac 1:16-22; Ac 2:14-40; Ac 3:12-26; Ac 4:8-12; Ac 10:34-43; Ac 11:4-17; Ac 15:7-11")
    lines.append("| check | target share | comparison mean | p |")
    lines.append("|---|---|---|---|")
    checks = [("D1 without ἀνήρ (speech address formula)", others, no_address),
              ("D1 against Peter's speeches only", peter, pauline),
              ("D1 against Peter's speeches only, without ἀνήρ", peter, no_address),
              ("D1 with words Pauline but not Lukan", others, pauline_only)]
    for label, pool, words in checks:
        observed, mean, p, hits, size = permutation(paul, pool, words)
        lines.append(f"| {label} | {100 * observed:.2f}% | {100 * mean:.2f}% | {p:.4f} |")
    lines.append("")
    lines.append(f"Words that are Pauline but not Lukan ({len(pauline_only)}), share of each text:")
    lines.append("")
    lines.append("| text | share |")
    lines.append("|---|---|")
    groups = [("the seven letters (minus life-story passages)", pauline_base),
              ("Luke", passages("Lk 1:1-24:53")),
              ("Acts 1-12, narrative", without_speeches("Ac 1:1-12:25")),
              ("Acts, speeches other than Paul's", others),
              ("Acts 13-28, narrative", without_speeches("Ac 13:1-28:31")),
              ("Acts, Paul's speeches", paul)]
    for label, segments in groups:
        hits, size = share(segments, pauline_only)
        lines.append(f"| {label} | {100 * hits / size:.2f}% |")
    lines.append("")
    return lines


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    reference = books_without(REFERENCE, "")
    mark_reference = books_without(MARK_REFERENCE, "")
    pauline_base = books_without(PAUL, AUTOBIOGRAPHY)
    lukan_base = passages(ACTS_WITHOUT_PAUL) + books_without(["Lk"], "")
    mark_base = books_without(["Mk"], "")
    letters_rest = books_without(PAUL, AUTOBIOGRAPHY + "; " + GENRE_CONTROL)

    tests = [
        ("C", "Markan words: Luke's Markan blocks vs his other blocks", mark_base, mark_reference,
         passages(LUKE_FROM_MARK), passages(LUKE_NOT_MARK)),
        ("D1", "Pauline words: Paul's speeches in Acts vs other speeches in Acts", pauline_base, reference,
         passages(PAUL_SPEECHES), passages(OTHER_SPEECHES)),
        ("D2", "Lukan words: letters' autobiographical passages vs rest of the letters", lukan_base, reference,
         passages(AUTOBIOGRAPHY), letters_rest),
        ("G", "Lukan words: letters' non-Acts narrative passages vs rest of the letters", lukan_base, reference,
         passages(GENRE_CONTROL), letters_rest),
    ]
    lines = ["# Which came first, Acts or the letters? Part A results", "",
             "Rules: PREDICTIONS.md (SHA-256 d285a3a1…cb8bcb) and AMENDMENTS.md. Generated by acts_order.py. "
             f"Characteristic words: at least {MIN_COUNT} uses in the base text and at least {RATIO} times the "
             f"reference rate. p from {DRAWS:,} matched random draws (seed {SEED}).", "",
             "## Leakage tests", "",
             "| test | words in list | target share | comparison mean | ratio | p | hits / words |",
             "|---|---|---|---|---|---|---|"]
    details = []
    outcome = {}
    for name, label, base, ref, target, pool in tests:
        words = characteristic(base, ref, RATIO)
        observed, mean, p, hits, size = permutation(target, pool, words)
        outcome[name] = (observed, mean, p)
        ratio = observed / mean if mean else float("inf")
        lines.append(f"| {name}: {label} | {len(words)} | {100 * observed:.2f}% | {100 * mean:.2f}% | {ratio:.2f} | "
                     f"{p:.4f} | {hits} / {size} |")
        details.append(f"- **{name}** characteristic words found in the target: {hit_words(target, words)}")
    lines.append("")
    lines.append("D2 counts as evidence only if p < 0.05 and the D2 target share is higher than the G target share "
                 "(PREDICTIONS.md section 3).")
    d2_counts = outcome["D2"][2] < 0.05 and outcome["D2"][0] > outcome["G"][0]
    lines.append("")
    lines.append(f"- C (method works, p < 0.01): **{'yes' if outcome['C'][2] < 0.01 else 'no'}**")
    lines.append(f"- D1 (p < 0.05): **{'yes' if outcome['D1'][2] < 0.05 else 'no'}**")
    lines.append(f"- D2 (p < 0.05 and above the genre control): **{'yes' if d2_counts else 'no'}**")
    lines.append("")
    lines.append("## Which words carry each result")
    lines.append("")
    lines.extend(details)
    lines.append("")

    lines.append("## Sensitivity: other thresholds (reported, not decisive)")
    lines.append("")
    lines.append("| test | ratio threshold | words in list | target share | comparison mean | p |")
    lines.append("|---|---|---|---|---|---|")
    for threshold in SENSITIVITY:
        for name, label, base, ref, target, pool in tests:
            words = characteristic(base, ref, threshold)
            observed, mean, p, hits, size = permutation(target, pool, words)
            lines.append(f"| {name} | {threshold} | {len(words)} | {100 * observed:.2f}% | {100 * mean:.2f}% | "
                         f"{p:.4f} |")
    lines.append("")

    reference_set = trigrams(reference, "")
    letters = letters_trigrams()
    acts_shared = shared_phrases("Ac", letters, reference_set)
    luke_shared = shared_phrases("Lk", letters, reference_set)
    acts_total = len(trigrams([book("Ac")], ""))
    luke_total = len(trigrams([book("Lk")], ""))
    lines.append("## Part A2: three-lemma phrases shared with the seven letters and absent from the reference books")
    lines.append("")
    lines.append(f"- Acts and the letters: **{len(acts_shared)}** phrases (Acts has {acts_total:,} distinct phrases)")
    lines.append(f"- Luke and the letters: **{len(luke_shared)}** phrases (Luke has {luke_total:,} distinct phrases)")
    lines.append("")
    for title, shared, name in [("Acts", acts_shared, "Ac"), ("Luke", luke_shared, "Lk")]:
        lines.append(f"### {title} and the letters")
        lines.append("")
        lines.append(f"| phrase (lemmas) | {name} | letters |")
        lines.append("|---|---|---|")
        for key, text_places, paul_where in shared:
            lines.append(f"| {' '.join(key)} | {', '.join(text_places)} | {', '.join(paul_where)} |")
        lines.append("")
    lines.extend(exploratory(reference, pauline_base, lukan_base))
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines[:20]))
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
