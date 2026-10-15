"""Blind test with longer samples: each book cut into back-to-back blocks of about 1,500 words
(short books kept whole if under 1,500). Same stronger features as blind_rich.py, no names."""
import numpy as np, re
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import adjusted_rand_score as ari
import blind_rich as R    # reuses its word and grammar-tag lists
SIZE = 1500
Wb, Tb = {}, {}
for l in R.labels:
    b = R.book(l); Wb.setdefault(b, []).extend(R.W[l]); Tb.setdefault(b, []).extend(R.T[l])
labs, words, tags = [], [], []
for b in Wb:
    n = max(1, round(len(Wb[b]) / SIZE)); cut = np.linspace(0, len(Wb[b]), n + 1).astype(int)
    for i in range(n):
        labs.append(f"{b}_{i+1}"); words.append(Wb[b][cut[i]:cut[i+1]]); tags.append(Tb[b][cut[i]:cut[i+1]])
chars = [[s[i:i+3] for i in range(len(s) - 2)] for s in (" " + " ".join(v) + " " for v in words)]
tagbi = [[a + "_" + b for a, b in zip(v, v[1:])] for v in tags]
X = np.hstack([R.rel(words, 300), R.rel(chars, 500), R.rel(tagbi, 200)])
B = [l.split("_")[0] for l in labs]; A = [R.GROUP[b] for b in B]
L = linkage(pdist(X, "cosine"), "ward")
print(f"\n=== {len(labs)} blocks of about {SIZE} words, no names ===")
for k in (8, 12):
    print(f"{k} groups: match author {ari(A, fcluster(L, k, 'maxclust')):.2f}")
c = fcluster(L, 8, "maxclust")
for g in sorted(set(c)):
    m = [B[i] for i in range(len(B)) if c[i] == g]
    print(f"  {len(m):>3}  {dict(Counter(m).most_common(8))}")
D = squareform(pdist(X, "cosine")); np.fill_diagonal(D, np.inf); nn = D.argmin(1)
multi = [i for i in range(len(B)) if B.count(B[i]) > 1]
print(f"Closest block is from the same book: {np.mean([B[i]==B[nn[i]] for i in multi]):.0%}")
print(f"Closest block is the same traditional author: {np.mean([A[i]==A[nn[i]] for i in range(len(B))]):.0%}")
core = {"Ro", "1Co", "2Co", "Ga"}
ci = [i for i in range(len(B)) if B[i] in core]
print(f"Core Paul blocks ({len(ci)}) whose closest block is core Paul: {np.mean([B[nn[i]] in core for i in ci]):.0%}")
def nn_other(i):
    d = D[i].copy(); d[[j for j in range(len(B)) if B[j] == B[i]]] = np.inf; return d.argmin()
print(f"Same, but the closest block must come from a DIFFERENT letter: {np.mean([B[nn_other(i)] in core for i in ci]):.0%}")
print("   (their closest other-letter match:", dict(Counter(B[nn_other(i)] for i in ci)), ")")
print("Core Paul blocks by blind group:", dict(Counter(c[i] for i in ci)))
