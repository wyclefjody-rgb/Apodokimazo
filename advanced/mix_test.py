"""Gray Eyes: 'when someone has written about 70% or more of a text it will consistently side with that author.'
Test: blend Paul with another writer at different shares, at chapter length (400 words) and 1,500 words.
Does the blend 'side with' Paul? Fair version: blend pieces and reference profiles come from DIFFERENT text
(Paul pieces from Romans, Paul reference = 1-2 Cor + Gal; other writer's pieces from one half, reference = other half).
100 MFW (whole NT), Eder's Simple. 400 random blends per setting."""
import sys, os, numpy as np
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load
ch = load("chapter"); keys = list(ch)
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
IDX = {w: i for i, w in enumerate(mfw)}
def ids(t): return np.array([IDX.get(w, -1) for w in t])
def P(a, n): return np.sqrt(np.bincount(a[a >= 0], minlength=100) / n)
book = lambda b, lo=1, hi=99: sum((ch[k] for k in keys if k.split()[0] == b and lo <= int(k.split()[1]) <= hi), [])
OTHERS = {"Hebrews": ("Heb", 1, 6, 7, 13), "Acts (speeches+narr.)": ("Ac", 1, 14, 15, 28)}
A_src = ids(book("Ro")); A_ref = book("1Co") + book("2Co") + book("Ga"); A_refP = P(ids(A_ref), len(A_ref))
rng = np.random.default_rng(5)
def piece(a, n): s = rng.integers(0, len(a) - n); return a[s:s + n]
for name, (b, s1, e1, s2, e2) in OTHERS.items():
    B_src = ids(book(b, s1, e1)); B_ref = book(b, s2, e2); B_refP = P(ids(B_ref), len(B_ref))
    print(f"\nPaul (Romans) blended with {name}:")
    print(f"{'Paul share':>10s} | {'400 words: sides with Paul':>27s} | {'1,500 words':>11s}")
    for share in (0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        row = []
        for N in (400, 1500):
            hits = 0
            for _ in range(400):
                na = int(round(N * share)); parts = []
                if na: parts.append(piece(A_src, na))
                if N - na: parts.append(piece(B_src, N - na))
                p = P(np.concatenate(parts), N)
                hits += np.abs(p - A_refP).sum() < np.abs(p - B_refP).sum()
            row.append(hits / 400)
        print(f"{int(share*100):>9d}% | {row[0]:>27.0%} | {row[1]:>11.0%}")
