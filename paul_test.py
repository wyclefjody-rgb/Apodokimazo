"""
    In total, this is meant to do something Eder's R package cannot do. Which is running 
"""

import sys
from collections import Counter
from itertools import combinations
from operator import itemgetter
from pathlib import Path

import numpy as np

CORPUS_DIR = Path("corpus_nt_books")
UNDISPUTED = ["Ro", "1Co", "2Co", "Ga", "Php", "1Th", "Phm"]
MAJOR_FOUR = ["Ro", "1Co", "2Co", "Ga"]
LETTERS = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit",
           "Phm", "Heb", "Jas", "1Pe", "2Pe", "1Jn", "23Jn", "Jud"]
MFW_COUNT = 100
SAMPLE_LENGTH = 1400
DRAWS = 200
SEED = 0


def load_books():
    files = sorted(CORPUS_DIR.glob("*.txt"))
    if not files:
        sys.exit(f"No texts found in '{CORPUS_DIR}'. Make sure to run make_corpus.py first then come back here.")

    books = {}
    for path in files:
        name = path.name.split("_")[0]
        books[name] = path.read_text(encoding="utf-8").split()
    return books


def most_frequent_words(texts, n):
    counts = Counter()
    for words in texts.values():
        counts.update(words)

    ranked = sorted(counts.items())
    ranked = sorted(ranked, key=itemgetter(1), reverse=True)
    vocabulary = []
    for word, _ in ranked[:n]:
        vocabulary.append(word)
    return vocabulary


def eder_distances(texts, names, vocabulary):
    profiles = []
    for name in names:
        words = texts[name]
        counts = Counter(words)
        shares = []
        for word in vocabulary:
            shares.append(counts[word] / len(words))
        profiles.append(shares)

    profiles = np.sqrt(np.array(profiles))
    differences = np.abs(profiles[:, None, :] - profiles[None, :, :])
    return differences.sum(axis=-1)


def spread(distances, position, group):
    pair_distances = []
    for first, second in combinations(group, 2):
        pair_distances.append(distances[position[first], position[second]])
    return np.mean(pair_distances)


def share_at_least_as_tight(distances, position, group, pool):
    target = spread(distances, position, group)

    as_tight = []
    for other_group in combinations(pool, len(group)):
        as_tight.append(spread(distances, position, other_group) <= target)

    return target, np.mean(as_tight), len(as_tight)


def nearest_letter(distances, position, letter, pool):
    best = None
    for other in pool:
        if other == letter:
            continue
        current = distances[position[letter], position[other]]
        if best is None or current < distances[position[letter], position[best]]:
            best = other
    return best


def equal_length_distances(books, pool, vocabulary, rng):
    samples = {}
    for name in pool:
        start = rng.integers(0, len(books[name]) - SAMPLE_LENGTH + 1)
        samples[name] = books[name][start:start + SAMPLE_LENGTH]
    return eder_distances(samples, pool, vocabulary)


def print_nearest_books(books, names, distances, position):
    print("Nearest other book for each undisputed letter (their settings):")
    for letter in UNDISPUTED:
        nearest = []
        for j in np.argsort(distances[position[letter]]):
            if names[j] != letter:
                nearest.append(names[j])
        print(f"  {letter:4s} -> {', '.join(nearest[:3])}   ({len(books[letter]):,} words)")


def print_group_test(distances, position, group, label):
    tightness, share, checked = share_at_least_as_tight(distances, position, group, LETTERS)
    print(f"\n{label}")
    print(f"  average distance within the group: {tightness:.3f}")
    print(f"  groups of {len(group)} letters checked: {checked:,}")
    print(f"  share of groups at least as tight: {share:.2%}")


def equal_length_check(books, pool, pauline, vocabulary, rng):
    position = {}
    for i, name in enumerate(pool):
        position[name] = i

    shares = []
    paired_with_paul = Counter()
    for draw in range(DRAWS):
        distances = equal_length_distances(books, pool, vocabulary, rng)
        shares.append(share_at_least_as_tight(distances, position, pauline, pool)[1])
        for letter in pauline:
            if nearest_letter(distances, position, letter, pool) in pauline:
                paired_with_paul[letter] += 1

    print(f"\nEqual-length check: {SAMPLE_LENGTH:,}-word samples from each letter, {DRAWS} random draws")
    print(f"  letters in the pool: {', '.join(pool)}")
    print(f"  share of groups of {len(pauline)} at least as tight as Paul's (average): {np.mean(shares):.2%}")
    print("  how often each Pauline letter's closest match is another Pauline letter:")
    for letter in pauline:
        print(f"    {letter:4s} {paired_with_paul[letter] / DRAWS:.0%}")

    chance = (len(pauline) - 1) / (len(pool) - 1)
    print(f"  (by pure chance a letter would pick another Pauline letter {chance:.0%} of the time)")


def major_four_check(books, pool, vocabulary, rng):
    position = {}
    for i, name in enumerate(pool):
        position[name] = i

    shares = []
    for draw in range(DRAWS):
        distances = equal_length_distances(books, pool, vocabulary, rng)
        shares.append(share_at_least_as_tight(distances, position, MAJOR_FOUR, pool)[1])

    group_count = len(list(combinations(pool, len(MAJOR_FOUR))))

    tightest = []
    for share in shares:
        tightest.append(share <= 1 / group_count)

    print(f"\nFour major letters ({', '.join(MAJOR_FOUR)}), {SAMPLE_LENGTH:,} words each:"
          + f"\nshare of the {group_count} possible groups of 4 at least as tight: {np.mean(shares):.2%}"
          + f"\ndraws where they were the single tightest group: {np.mean(tightest):.0%}")


def main():
    books = load_books()
    vocabulary = most_frequent_words(books, MFW_COUNT)

    names = list(books)
    position = {}
    for i, name in enumerate(names):
        position[name] = i
    distances = eder_distances(books, names, vocabulary)

    print_nearest_books(books, names, distances, position)

    without_philemon = []
    for letter in UNDISPUTED:
        if letter != "Phm":
            without_philemon.append(letter)

    print_group_test(distances, position, UNDISPUTED,
                     "Seven undisputed letters vs. every group of 7 NT letters")
    print_group_test(distances, position, without_philemon,
                     f"Without Philemon (only {len(books['Phm'])} words, too short to measure well)")

    pool = []
    for letter in LETTERS:
        if len(books[letter]) >= SAMPLE_LENGTH:
            pool.append(letter)

    pauline = []
    for letter in without_philemon:
        if letter in pool:
            pauline.append(letter)

    rng = np.random.default_rng(SEED)
    equal_length_check(books, pool, pauline, vocabulary, rng)
    major_four_check(books, pool, vocabulary, rng)


if __name__ == "__main__":
    main()