"""Gray Eyes' suggestion: would random ("grab bag") sampling beat contiguous stretches for short samples?
Same task as mfw_and_length.py: which of 9 known Greek authors wrote a sample from a work the method never saw
(chance 11%), Eder's Simple, 100 MFW. Compare:
  contiguous: n consecutive words (what a chapter is)
  grab bag:   n words drawn at random from across the whole held-out work (not possible for a single chapter,
              because a 400-word chapter only has its own 400 words)."""
import numpy as np
from collections import Counter
from common import AUTH, chunk
rng = np.random.default_rng(5); A = list(AUTH)
VOCAB = [w for w, _ in Counter(w for a in A for t in AUTH[a].values() for w in t).most_common(100)]
def prof(t): c = Counter(t); n = len(t); return np.sqrt(np.array([c[w] / n for w in VOCAB]))
print(f"{'sample':>8} | {'contiguous':>10} | {'grab bag':>8}")
for n in (100, 200, 400, 700, 1500):
    h = {"c": [], "g": []}
    for trial in range(15):
        held = {a: rng.choice(list(AUTH[a])) for a in A}
        ref = {a: prof(sum((t for w, t in AUTH[a].items() if w != held[a]), [])) for a in A}
        for a in A:
            work = AUTH[a][held[a]]
            for _ in range(3):
                for kind, x in (("c", chunk(work, n, rng)), ("g", list(rng.choice(work, n, replace=False)))):
                    p = prof(x); h[kind].append(min(A, key=lambda b: np.abs(p - ref[b]).sum()) == a)
    print(f"{n:>5} wd | {np.mean(h['c']):>10.0%} | {np.mean(h['g']):>8.0%}", flush=True)
