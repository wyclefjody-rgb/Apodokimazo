"""
    attic_hands: can stylometry find a hidden second hand inside a famous author's corpus (Apollodorus inside
    Demosthenes), or one writer behind many characters' voices (Lysias)? And does the same procedure single out any
    of Paul's core four? Rules in attic_hands/PREDICTIONS.md (SHA-256 47f9e83a…adf) and AMENDMENTS.md.

    Needs canonical-greekLit/ with the orators (python attic_hands/fetch_texts.py) and sblgnt/.

    Output: RESULTS.md.

    Usage (from the kit folder):   python -X utf8 attic_hands/attic_hands.py
"""
import os
import sys
from glob import glob

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(KIT, "advanced"))
import extract

PERSEUS = os.path.join(KIT, "canonical-greekLit", "data")
SBLGNT = os.path.join(KIT, "sblgnt")
OUTPUT = os.path.join(HERE, "RESULTS.md")
SIZE = 1000
FEATURES = 150

DEM_PRIVATE = [27, 28, 29, 30, 31, 36, 37, 38, 39, 41, 54, 55, 57]
DEM_PUBLIC = [1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24]
APOLLODORUS = [46, 49, 50, 52, 53, 59]
DISPUTED = [45, 47]
LYSIAS_EXCLUDED = [2, 6, 8, 9, 11, 15, 20, 33, 34]
OTHERS = [("Isaeus", "tlg0017", list(range(1, 13))), ("Antiphon", "tlg0028", [1, 5, 6]),
          ("Andocides", "tlg0027", [1, 2, 3]), ("Aeschines", "tlg0026", [1, 2, 3]),
          ("Isocrates (forensic)", "tlg0010", [1, 2, 3, 4, 5, 6])]
PAUL = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit", "Phm"]
CORE = ["Ro", "1Co", "2Co", "Ga"]
PASTORALS = ["1Ti", "2Ti", "Tit"]


def speech(author, number):
    paths = glob(os.path.join(PERSEUS, author, f"tlg{number:03d}", f"{author}.tlg{number:03d}.*grc*.xml"))
    if not paths:
        sys.exit(f"Missing {author} speech {number}. Run: python attic_hands/fetch_texts.py")
    return extract.load(paths[0])


def passages(words, keep_short=False):
    pieces = []
    for start in range(0, len(words) - SIZE + 1, SIZE):
        pieces.append(words[start:start + SIZE])
    if not pieces and keep_short and words:
        pieces.append(words)
    return pieces


def paul_letter(book):
    paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
    if not paths:
        sys.exit(f"No MorphGNT file for {book}. Run setup_data.py first.")
    words = []
    with open(paths[0], encoding="utf8") as file:
        for line in file:
            word = extract.norm(line.split()[4])
            if word:
                words.append(word)
    return words


def feature_list(all_passages):
    counts = {}
    for piece in all_passages:
        for word in piece:
            counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts.items(), key=count_then_word)
    chosen = []
    for word, count in ranked[:FEATURES]:
        chosen.append(word)
    return chosen


def count_then_word(item):
    return (-item[1], item[0])


def zscores(all_passages, features):
    index = {}
    for position, word in enumerate(features):
        index[word] = position
    matrix = np.zeros((len(all_passages), len(features)))
    for row, piece in enumerate(all_passages):
        for word in piece:
            if word in index:
                matrix[row, index[word]] += 1
        matrix[row] /= len(piece)
    mean = matrix.mean(axis=0)
    spread = matrix.std(axis=0)
    spread[spread == 0] = 1.0
    return (matrix - mean) / spread


def cosine_distance(first, second):
    norm = np.linalg.norm(first) * np.linalg.norm(second)
    if norm == 0:
        return 1.0
    return 1.0 - float(np.dot(first, second) / norm)


def auc(scores, labels):
    """Share of (other-hand, genuine) pairs in which the other-hand text has the larger score; ties count half."""
    positives = []
    negatives = []
    for score, label in zip(scores, labels):
        if label:
            positives.append(score)
        else:
            negatives.append(score)
    total = 0.0
    for high in positives:
        for low in negatives:
            if high > low:
                total += 1.0
            elif high == low:
                total += 0.5
    return total / (len(positives) * len(negatives))


def outlier_ranking(texts):
    """texts: list of (name, words, keep_short). Each text's mean Cosine Delta distance to every other text
    (AMENDMENTS.md 2). Returns [(name, distance)] sorted, largest first."""
    owners = []
    pieces = []
    for name, words, keep_short in texts:
        for piece in passages(words, keep_short):
            owners.append(name)
            pieces.append(piece)
    features = feature_list(pieces)
    matrix = zscores(pieces, features)
    names = []
    for name, words, keep_short in texts:
        if name in owners and name not in names:
            names.append(name)
    centroids = {}
    for name in names:
        rows = []
        for row, owner in enumerate(owners):
            if owner == name:
                rows.append(row)
        centroids[name] = matrix[rows].mean(axis=0)
    result = []
    for name in names:
        total = 0.0
        for other in names:
            if other != name:
                total += cosine_distance(centroids[name], centroids[other])
        result.append((name, total / (len(names) - 1)))
    result.sort(key=second_item, reverse=True)
    return result


def core_profiles(texts):
    """Each text's mean Cosine Delta distance to the core four (a core letter: to the other three)."""
    owners = []
    pieces = []
    for name, words, keep_short in texts:
        for piece in passages(words, keep_short):
            owners.append(name)
            pieces.append(piece)
    features = feature_list(pieces)
    matrix = zscores(pieces, features)
    centroids = {}
    for name, words, keep_short in texts:
        rows = []
        for row, owner in enumerate(owners):
            if owner == name:
                rows.append(row)
        if rows:
            centroids[name] = matrix[rows].mean(axis=0)
    result = []
    for name in centroids:
        total = 0.0
        count = 0
        for core in CORE:
            if core != name:
                total += cosine_distance(centroids[name], centroids[core])
                count += 1
        result.append((name, total / count))
    result.sort(key=second_item, reverse=True)
    return result


def second_item(item):
    return item[1]


def attribution(writers):
    """writers: {writer: [(speech, words)]}. Leave-one-speech-out nearest centroid."""
    owners = []
    speeches = []
    pieces = []
    for writer, items in writers.items():
        for label, words in items:
            for piece in passages(words):
                owners.append(writer)
                speeches.append(label)
                pieces.append(piece)
    features = feature_list(pieces)
    matrix = zscores(pieces, features)
    results = {}
    for label in sorted(set(speeches), key=speeches.index):
        rows = []
        for row, item in enumerate(speeches):
            if item == label:
                rows.append(row)
        centroids = {}
        for writer in writers:
            members = []
            for row, owner in enumerate(owners):
                if owner == writer and speeches[row] != label:
                    members.append(row)
            if members:
                centroids[writer] = matrix[members].mean(axis=0)
        votes = {}
        for row in rows:
            best = None
            best_distance = None
            for writer, centroid in centroids.items():
                distance = cosine_distance(matrix[row], centroid)
                if best_distance is None or distance < best_distance:
                    best = writer
                    best_distance = distance
            votes[best] = votes.get(best, 0) + 1
        results[label] = (owners[rows[0]], votes, len(rows))
    return results


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    lines = ["# attic_hands: results", "",
             "Rules: PREDICTIONS.md (SHA-256 47f9e83a104f371aa1f348d9bf2091b5ffc771a67438e236267cb78ebcdd8adf) and "
             "AMENDMENTS.md. Generated by attic_hands.py. Passages of 1,000 words; the 150 most frequent words of each "
             "analysis; Cosine Delta.", ""]

    writers = {"Lysias": [], "Demosthenes (private)": [], "Apollodorus": []}
    for number in range(1, 35):
        if number in LYSIAS_EXCLUDED:
            continue
        words = speech("tlg0540", number)
        if len(words) >= SIZE:
            writers["Lysias"].append((f"Lysias {number}", words))
    for number in DEM_PRIVATE:
        writers["Demosthenes (private)"].append((f"Dem. {number}", speech("tlg0014", number)))
    for number in APOLLODORUS:
        writers["Apollodorus"].append((f"[Dem.] {number}", speech("tlg0014", number)))
    for name, author, numbers in OTHERS:
        writers[name] = []
        for number in numbers:
            writers[name].append((f"{name} {number}", speech(author, number)))

    results = attribution(writers)
    lines.append("## A. Lysias under many voices: leave-one-speech-out attribution among 8 writers (chance 12.5%)")
    lines.append("")
    lines.append("| writer | speeches | passages | passages to the right writer | speeches to the right writer |")
    lines.append("|---|---|---|---|---|")
    lysias_passages = 0.0
    lysias_speeches = 0.0
    for writer in writers:
        right_passages = 0
        total_passages = 0
        right_speeches = 0
        total_speeches = 0
        for label, (owner, votes, count) in results.items():
            if owner != writer:
                continue
            total_speeches += 1
            total_passages += count
            right_passages += votes.get(writer, 0)
            winner = max(votes.items(), key=second_item)[0]
            if winner == writer:
                right_speeches += 1
        if total_speeches == 0:
            continue
        share_p = 100.0 * right_passages / total_passages
        share_s = 100.0 * right_speeches / total_speeches
        if writer == "Lysias":
            lysias_passages = share_p
            lysias_speeches = share_s
        lines.append(f"| {writer} | {total_speeches} | {total_passages} | {right_passages} ({share_p:.0f}%) | "
                     f"{right_speeches} ({share_s:.0f}%) |")
    lines.append("")
    met_a = lysias_passages >= 60 and lysias_speeches >= 70
    lines.append(f"Prediction A (Lysias: at least 60% of passages and 70% of speeches): {'met' if met_a else 'not met'}.")
    lines.append("")
    lines.append("Lysias's speeches one by one (votes of their passages):")
    lines.append("")
    for label, (owner, votes, count) in results.items():
        if owner == "Lysias":
            shown = []
            for writer, number in sorted(votes.items(), key=second_item, reverse=True):
                shown.append(f"{writer} {number}")
            lines.append(f"- {label} ({count} passages): {', '.join(shown)}")
    lines.append("")

    lines.append("## B. Apollodorus inside Demosthenes: unlabelled outlier ranking")
    lines.append("")
    corpus = []
    labels = {}
    for number in DEM_PRIVATE:
        corpus.append((f"Dem. {number}", speech("tlg0014", number), False))
        labels[f"Dem. {number}"] = False
    for number in APOLLODORUS:
        corpus.append((f"[Dem.] {number} (Apollodorus)", speech("tlg0014", number), False))
        labels[f"[Dem.] {number} (Apollodorus)"] = True
    ranking = outlier_ranking(corpus)
    scores = []
    flags = []
    genuine_max = 0.0
    for name, distance in ranking:
        scores.append(distance)
        flags.append(labels[name])
        if not labels[name]:
            genuine_max = max(genuine_max, distance)
    value_b = auc(scores, flags)
    beyond = 0
    for name, distance in ranking:
        if labels[name] and distance > genuine_max:
            beyond += 1
    lines.append("| rank | speech | mean distance to the other speeches |")
    lines.append("|---|---|---|")
    for position, (name, distance) in enumerate(ranking, 1):
        lines.append(f"| {position} | {name} | {distance:.3f} |")
    lines.append("")
    lines.append(f"AUC (Apollodorus against genuine): {value_b:.2f}. Prediction B1 (at least 0.80): "
                 f"{'met' if value_b >= 0.80 else 'not met'}.")
    lines.append(f"Apollodoran speeches beyond the most distant genuine speech: {beyond} of {len(APOLLODORUS)}. "
                 f"Prediction B2 (at least 4): {'met' if beyond >= 4 else 'not met'}.")
    lines.append("")
    lines.append("### Exploratory: the disputed speeches 45 and 47, and the public speeches added")
    lines.append("")
    extended = list(corpus)
    for number in DISPUTED:
        extended.append((f"[Dem.] {number} (disputed)", speech("tlg0014", number), False))
    ranking = outlier_ranking(extended)
    shown = []
    for position, (name, distance) in enumerate(ranking, 1):
        if "disputed" in name:
            shown.append(f"{name}: rank {position} of {len(ranking)}")
    lines.append("With 45 and 47 added: " + "; ".join(shown) + ".")
    lines.append("")
    public = list(corpus)
    for number in DEM_PUBLIC:
        public.append((f"Dem. {number} (public)", speech("tlg0014", number), False))
    ranking = outlier_ranking(public)
    scores = []
    flags = []
    top = []
    for position, (name, distance) in enumerate(ranking, 1):
        scores.append(distance)
        flags.append("Apollodorus" in name)
        if position <= 10:
            top.append(name)
    lines.append(f"With the public speeches added ({len(ranking)} speeches): AUC for Apollodorus {auc(scores, flags):.2f}. "
                 f"The ten most distant: {', '.join(top)}.")
    lines.append("")

    lines.append("## C. The same ranking on Paul's 13 letters")
    lines.append("")
    letters = []
    for book in PAUL:
        letters.append((book, paul_letter(book), True))
    ranking = outlier_ranking(letters)
    scores = []
    flags = []
    lines.append("| rank | letter | words | mean distance to the other letters |")
    lines.append("|---|---|---|---|")
    sizes = {}
    for book, words, keep in letters:
        sizes[book] = len(words)
    core_places = []
    for position, (name, distance) in enumerate(ranking, 1):
        scores.append(distance)
        flags.append(name in PASTORALS)
        if name in CORE:
            core_places.append(position)
        lines.append(f"| {position} | {name} | {sizes[name]:,} | {distance:.3f} |")
    lines.append("")
    value_c = auc(scores, flags)
    lines.append(f"AUC (Pastorals against the other ten): {value_c:.2f}. Prediction C1 (at least 0.80): "
                 f"{'met' if value_c >= 0.80 else 'not met'}.")
    places = []
    for place in core_places:
        places.append(str(place))
    lines.append(f"Core four's places: {', '.join(places)}. "
                 f"Prediction C2 (none among the four most distant): {'met' if min(core_places) > 4 else 'not met'}.")
    lines.append("")
    lines.append("### Exploratory (AMENDMENTS.md 3): distance from the core four")
    lines.append("")
    lines.append("Each letter's mean distance to the core four (for a core letter, to the other three). Same features and "
                 "z-scores as above.")
    lines.append("")
    profiles = core_profiles(letters)
    lines.append("| rank | letter | mean distance to the core four |")
    lines.append("|---|---|---|")
    for position, (name, distance) in enumerate(profiles, 1):
        lines.append(f"| {position} | {name} | {distance:.3f} |")
    lines.append("")
    core_scores = []
    core_flags = []
    for name, distance in profiles:
        if name not in CORE:
            core_scores.append(distance)
            core_flags.append(name in PASTORALS)
    lines.append(f"AUC (Pastorals against the other six letters outside the core four): {auc(core_scores, core_flags):.2f}.")
    lines.append("")
    with open(OUTPUT, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {OUTPUT}")


if __name__ == "__main__":
    main()
