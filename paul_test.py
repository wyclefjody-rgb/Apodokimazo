"""Does Paul look like one voice or a committee?
Compares the seven letters most scholars accept as Paul's against every other possible
group of seven New Testament letters, using the book's own settings
(100 most frequent words, Eder's Simple distance). Run after make_corpus.py:
    python3 paul_test.py
"""
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import glob, itertools, os
import numpy as np
from collections import Counter

books = {os.path.basename(f).split("_")[0]: open(f, encoding="utf8").read().split()
         for f in glob.glob("corpus_nt_books/*.txt")}
UNDISPUTED = ["Ro", "1Co", "2Co", "Ga", "Php", "1Th", "Phm"]
LETTERS = ["Ro", "1Co", "2Co", "Ga", "Eph", "Php", "Col", "1Th", "2Th", "1Ti", "2Ti", "Tit",
           "Phm", "Heb", "Jas", "1Pe", "2Pe", "1Jn", "23Jn", "Jud"]

top = [w for w, _ in Counter(t for v in books.values() for t in v).most_common(100)]
names = list(books)
X = np.array([[Counter(books[b])[w] / len(books[b]) for w in top] for b in names])
S = np.sqrt(X)
D = np.abs(S[:, None, :] - S[None, :, :]).sum(-1)   # Eder's Simple distance
ix = {b: i for i, b in enumerate(names)}


def spread(group):  # average distance between members; lower = more alike
    g = [ix[b] for b in group]
    return np.mean([D[a, b] for a, b in itertools.combinations(g, 2)])


def test(group, pool, label):
    real = spread(group)
    others = [spread(c) for c in itertools.combinations(pool, len(group))]
    rank = np.mean([o <= real for o in others])
    print(f"\n{label}")
    print(f"  average distance within the group: {real:.3f}")
    print(f"  groups of {len(group)} letters checked: {len(others):,}")
    print(f"  share of groups at least as tight: {rank:.2%}")
    return real, rank, len(others)


print("Nearest other book for each undisputed letter (their settings):")
for b in UNDISPUTED:
    order = [names[j] for j in np.argsort(D[ix[b]]) if names[j] != b]
    print(f"  {b:4s} -> {', '.join(order[:3])}   ({len(books[b]):,} words)")

r1 = test(UNDISPUTED, LETTERS, "Seven undisputed letters vs. every group of 7 NT letters")
six = [b for b in UNDISPUTED if b != "Phm"]
r2 = test(six, LETTERS, "Without Philemon (only 335 words, too short to measure well)")

# ---- Equal-length check: longer texts are measured more precisely, so big letters can look
# alike just because they are big. Here every letter contributes the same number of words.
L = 1400
pool = [b for b in LETTERS if len(books[b]) >= L]
grp = [b for b in six if b in pool]
rng = np.random.default_rng(0)
ranks, hits = [], Counter()
for rep in range(200):
    samp = {}
    for b in pool:
        o = rng.integers(0, len(books[b]) - L + 1)
        samp[b] = books[b][o:o + L]
    Xs = np.array([[Counter(samp[b])[w] / L for w in top] for b in pool])
    Ss = np.sqrt(Xs); Ds = np.abs(Ss[:, None] - Ss[None]).sum(-1)
    j = {b: i for i, b in enumerate(pool)}
    sp = lambda g: np.mean([Ds[j[a], j[c]] for a, c in itertools.combinations(g, 2)])
    real = sp(grp)
    ranks.append(np.mean([sp(c) <= real for c in itertools.combinations(pool, len(grp))]))
    for b in grp:
        nb = min((x for x in pool if x != b), key=lambda x: Ds[j[b], j[x]])
        hits[b] += nb in grp
print(f"\nEqual-length check: {L:,}-word samples from each letter, 200 random draws")
print(f"  letters in the pool: {', '.join(pool)}")
print(f"  share of groups of {len(grp)} at least as tight as Paul's (average): {np.mean(ranks):.2%}")
print(f"  how often each Pauline letter's closest match is another Pauline letter:")
for b in grp:
    print(f"    {b:4s} {hits[b] / 200:.0%}")
print(f"  (by pure chance a letter would pick another Pauline letter {(len(grp)-1)/(len(pool)-1):.0%} of the time)")

# ---- The four major letters on their own, same equal-length method
core = ["Ro", "1Co", "2Co", "Ga"]
ranks4 = []
for rep in range(200):
    samp = {b: books[b][(o := rng.integers(0, len(books[b]) - L + 1)):o + L] for b in pool}
    Xs = np.array([[Counter(samp[b])[w] / L for w in top] for b in pool])
    Ss = np.sqrt(Xs); Ds = np.abs(Ss[:, None] - Ss[None]).sum(-1)
    j = {b: i for i, b in enumerate(pool)}
    sp = lambda g: np.mean([Ds[j[a], j[c]] for a, c in itertools.combinations(g, 2)])
    real = sp(core)
    ranks4.append(np.mean([sp(c) <= real for c in itertools.combinations(pool, 4)]))
print(f"\nFour major letters (Ro, 1Co, 2Co, Ga), {L:,} words each:")
print(f"  share of the {len(list(itertools.combinations(pool, 4)))} possible groups of 4 at least as tight: {np.mean(ranks4):.2%}")
print(f"  draws where they were the single tightest group: {np.mean([r <= 1/715 for r in ranks4]):.0%}")
