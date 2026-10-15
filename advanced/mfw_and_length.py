"""Two questions in one table, on 9 Greek authors whose authorship is known:
  1. Is 100 most frequent words (MFW) enough, or do more help?      (columns)
  2. How short can a sample be?                                     (rows)
Task: which of the 9 authors wrote a sample taken from a work the method has never seen (chance = 11%).
Method: the book's own, Eder's Simple distance to each author's reference text."""
import numpy as np
from collections import Counter
from common import AUTH, chunk
rng = np.random.default_rng(5)
A = list(AUTH)
pool = Counter(w for a in A for t in AUTH[a].values() for w in t)
MFWS, SIZES = [50, 100, 200, 500, 1000], [100, 200, 400, 700, 1500, 2500]
VOCAB = [w for w, _ in pool.most_common(max(MFWS))]
def prof(tokens):
    c = Counter(tokens); n = len(tokens); return np.sqrt(np.array([c[w] / n for w in VOCAB]))
print(f"{'sample':>8} | " + " ".join(f"{m:>6} MFW" for m in MFWS))
for n in SIZES:
    hits = {m: [] for m in MFWS}
    for trial in range(15):
        held = {a: rng.choice(list(AUTH[a])) for a in A}
        ref = {a: prof(sum((t for w, t in AUTH[a].items() if w != held[a]), [])) for a in A}
        for a in A:
            for _ in range(3):
                x = prof(chunk(AUTH[a][held[a]], n, rng))
                for m in MFWS:
                    hits[m].append(min(A, key=lambda b: np.abs(x[:m] - ref[b][:m]).sum()) == a)
    print(f"{n:>5} wd | " + " ".join(f"{np.mean(hits[m]):>10.0%}" for m in MFWS), flush=True)
