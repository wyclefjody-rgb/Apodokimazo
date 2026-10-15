"""Paul's 61 undisputed chapters: is each one's closest chapter also Paul? Real text vs 20 runs of shuffled words.
Book's settings: single words, 100 most frequent words, Eder's Simple."""
from load import load, book_of, GROUP
from collections import Counter
import numpy as np
ch = load("chapter"); labs = list(ch); T = [ch[l] for l in labs]
B = [book_of(l) for l in labs]; G = [GROUP[b] for b in B]
def nn(T):
    top = [w for w, _ in Counter(t for v in T for t in v).most_common(100)]
    S = np.sqrt(np.array([[Counter(v)[w] / len(v) for w in top] for v in T])); D = np.abs(S[:, None] - S[None]).sum(-1)
    np.fill_diagonal(D, np.inf); return D.argmin(1)
P = [i for i, g in enumerate(G) if g == "Paul (undisputed)"]
def score(n):
    return (np.mean([B[n[i]] == B[i] for i in P]), np.mean([G[n[i]] == "Paul (undisputed)" for i in P]),
            np.mean([G[n[i]] == "Paul (undisputed)" and B[n[i]] != B[i] for i in P]))
real = score(nn(T)); rng = np.random.default_rng(0); allt = [t for v in T for t in v]; sh = []
for k in range(20):
    p = rng.permutation(allt); f, o = [], 0
    for v in T: f.append(list(p[o:o + len(v)])); o += len(v)
    sh.append(score(nn(f)))
sh = np.mean(sh, 0)
for lab, a, b in zip(["same letter", "any undisputed Paul", "a different undisputed letter"], real, sh):
    print(f"Closest chapter is from {lab:30s} real {a:.0%}   shuffled {b:.0%}")
