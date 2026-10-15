"""Blind test, stronger features. Same chapters, no names, but instead of the 100 most common words it uses:
  - 300 most common words
  - 500 most common 3-letter sequences (catches endings and small words, holds up better on short texts)
  - 200 most common grammar-tag pairs from MorphGNT (e.g. article+noun, participle+verb): style, not topic
Each feature set is standardized, joined, compared with cosine distance, and grouped with Ward.
Then, as before, the groups are checked against book, traditional author and genre."""
import glob, os, re, numpy as np
from collections import Counter, OrderedDict
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.metrics import adjusted_rand_score as ari
from load import strip, GROUP

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sblgnt")
W, T = OrderedDict(), OrderedDict()
for f in sorted(glob.glob(f"{SRC}/*-morphgnt.txt")):
    book = re.match(r"\d+-(\w+)-", os.path.basename(f)).group(1)
    book = "2-3Jn" if book in ("2Jn", "3Jn") else book
    for line in open(f, encoding="utf8"):
        ref, pos, parse, text, word, norm, lemma = line.split()
        key = book if book == "2-3Jn" else f"{book} {int(ref[2:4])}"
        W.setdefault(key, []).append(strip(norm))
        mood = parse[3] if parse[3] != "-" else ""
        T.setdefault(key, []).append(pos.strip("-") + mood)       # e.g. V + P(articiple), N-, RA
labels = list(W)
book = lambda l: l.split(" ")[0]
NARR = {"Mt", "Mk", "Lk", "Jn", "Ac"}
genre = lambda b: "narrative" if b in NARR else ("apocalypse" if b == "Re" else "letter")

def rel(units, n):
    top = [w for w, _ in Counter(u for v in units for u in v).most_common(n)]
    M = np.array([[Counter(v)[w] / max(len(v), 1) for w in top] for v in units])
    return (M - M.mean(0)) / (M.std(0) + 1e-12)

words = [W[l] for l in labels]
chars = [[s[i:i+3] for i in range(len(s) - 2)] for s in (" " + " ".join(v) + " " for v in words)]
tagbi = [[a + "_" + b for a, b in zip(v, v[1:])] for v in (T[l] for l in labels)]
X = np.hstack([rel(words, 300), rel(chars, 500), rel(tagbi, 200)])
L = linkage(pdist(X, "cosine"), "ward")
B = [book(l) for l in labels]; A = [GROUP[b] for b in B]; G = [genre(b) for b in B]
print("groups   match book   match author   match genre")
for k in (3, 5, 8, 12):
    c = fcluster(L, k, "maxclust")
    print(f"{k:>6}   {ari(B, c):>10.2f}   {ari(A, c):>12.2f}   {ari(G, c):>11.2f}")
c = fcluster(L, 8, "maxclust")
print("\nThe 8 blind groups:")
for g in sorted(set(c)):
    m = [B[i] for i in range(len(B)) if c[i] == g]
    print(f"  {len(m):>3}  {dict(Counter(m).most_common(7))}")
pc = Counter(c[i] for i in range(len(B)) if A[i] == "Paul (undisputed)")
print("\nUndisputed Paul's 61 chapters across blind groups:", sorted(pc.values(), reverse=True))
# nearest neighbour, as in the main test
Dm = np.array(pdist(X, "cosine")); from scipy.spatial.distance import squareform
Dm = squareform(Dm); np.fill_diagonal(Dm, np.inf); nn = Dm.argmin(1)
print(f"Closest chapter is from the same book: {np.mean([B[i]==B[nn[i]] for i in range(len(B))]):.0%} (their settings gave 52%)")
print(f"Closest chapter is the same traditional author: {np.mean([A[i]==A[nn[i]] for i in range(len(B))]):.0%}")
