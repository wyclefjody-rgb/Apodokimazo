"""
    mfw_and_length.py: accuracy of the book's method (Eder's Simple, 100 MFW) on
    9 Greek authors with known works, by sample length (rows) and number of MFW (columns).
    Each passage comes from a work held out from that author's reference. Chance = 11%.

    The range shows how much each number moves with the random choices alone.
"""
import sys
import numpy as np
from collections import Counter
from common import AUTH, chunk

N_SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 1   # how many runs (seeds 5, 6, 7, ...)
A = list(AUTH)
pool = Counter(w for a in A for t in AUTH[a].values() for w in t)
MFWS, SIZES = [50, 100, 200, 500, 1000], [100, 200, 400, 700, 1500, 2500]
VOCAB = [pair[0] for pair in pool.most_common(max(MFWS))]   # most frequent words, pooled across authors

def prof(tokens):
    """Eder's Simple profile: square-rooted share of each common word."""
    c = Counter(tokens)
    n = len(tokens)
    shares = [c[w] / n for w in VOCAB]
    return np.sqrt(np.array(shares))

def run(seed):
    """One full experiment: returns {sample length: {MFW: share correct}}."""
    rng = np.random.default_rng(seed)   # fixed seed so results are reproducible
    out = {}
    for n in SIZES:
        hits = {m: [] for m in MFWS}
        for trial in range(15):
            # hold out one work per author, reference = the author's other works
            held = {a: rng.choice(list(AUTH[a])) for a in A}
            ref = {a: prof(sum((t for w, t in AUTH[a].items() if w != held[a]), [])) for a in A}
            for a in A:
                for _ in range(3):
                    x = prof(chunk(AUTH[a][held[a]], n, rng))   # contiguous passage from the held-out work
                    for m in MFWS:
                        # nearest author by Eder's Simple distance, correct?
                        hits[m].append(min(A, key=lambda b: np.abs(x[:m] - ref[b][:m]).sum()) == a)
        out[n] = {m: np.mean(hits[m]) for m in MFWS}
    return out

# ---------- Output is one run (seed 5), or N runs averaged with lowest-highest ----------
# Instead of running just once, can run many times (Ran 100 times and is in mfw_100seeds.txt)
head = f"{'sample':>8} | " + " ".join(f"{m:>11} MFW" for m in MFWS)
if N_SEEDS == 1:
    r = run(5)
    print(f"{'sample':>8} | " + " ".join(f"{m:>6} MFW" for m in MFWS))
    for n in SIZES:
        print(f"{n:>5} wd | " + " ".join(f"{r[n][m]:>10.0%}" for m in MFWS), flush=True)
else:
    runs = []
    for i in range(N_SEEDS):
        runs.append(run(5 + i)); print(f"   run {i + 1}/{N_SEEDS} done (seed {5 + i})", flush=True)
    print(f"\nAverage over {N_SEEDS} seeds, with lowest-highest in brackets:")
    print(head)
    for n in SIZES:
        cells = []
        for m in MFWS:
            v = [r[n][m] for r in runs]
            cells.append(f"{np.mean(v):>4.0%} ({min(v):.0%}-{max(v):.0%})")
        print(f"{n:>5} wd | " + " ".join(f"{c:>15}" for c in cells))