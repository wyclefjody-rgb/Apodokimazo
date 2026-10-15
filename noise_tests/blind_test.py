"""Blind test: every New Testament chapter with NO names. Group them by style alone (the book's settings),
then only afterwards check what the groups line up with: book, traditional author, or genre."""
import numpy as np
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from sklearn.metrics import adjusted_rand_score as ari
from load import load, book_of, GROUP

NARR = {"Mt", "Mk", "Lk", "Jn", "Ac"}
genre = lambda b: "narrative" if b in NARR else ("apocalypse" if b == "Re" else "letter")

def tree(texts):
    top = [w for w, _ in Counter(t for v in texts for t in v).most_common(100)]
    S = np.sqrt(np.array([[Counter(v)[w] / len(v) for w in top] for v in texts]))
    D = np.abs(S[:, None] - S[None]).sum(-1)
    return D, linkage(squareform(D, checks=False), "ward")

rng = np.random.default_rng(0)
for level in ("chapter", "book"):
    ch = load(level)
    labels = list(ch)                       # kept aside; never shown to the clustering
    texts = [ch[l] for l in labels]
    order = rng.permutation(len(texts))     # scramble the order too, so position gives nothing away
    D, L = tree([texts[i] for i in order])
    labs = [labels[i] for i in order]
    B = [book_of(l) for l in labs]; A = [GROUP[b] for b in B]; G = [genre(b) for b in B]
    print(f"\n=== {level.upper()}S, no names ({len(labs)} texts) ===")
    print("groups   match book   match author   match genre     (1 = perfect, 0 = chance)")
    for k in (3, 5, 8, 12):
        c = fcluster(L, k, "maxclust")
        print(f"{k:>6}   {ari(B, c):>10.2f}   {ari(A, c):>12.2f}   {ari(G, c):>11.2f}")
    k = 3
    c = fcluster(L, k, "maxclust")
    print(f"\nWhat's in each of the {k} blind groups (by genre / author):")
    for g in sorted(set(c)):
        m = [i for i in range(len(labs)) if c[i] == g]
        print(f"  group {g} ({len(m)}): genre {dict(Counter(G[i] for i in m))}")
        print(f"            author {dict(Counter(A[i] for i in m).most_common(5))}")
    if level == "chapter":
        # shuffled baseline
        allt = [t for v in texts for t in v]; null = []
        for r in range(20):
            p = rng.permutation(allt); f, o = [], 0
            for v in texts: f.append(list(p[o:o+len(v)])); o += len(v)
            _, Lf = tree([f[i] for i in order])
            null.append([ari(x, fcluster(Lf, 8, "maxclust")) for x in (B, A, G)])
        print("\nShuffled words, 8 groups: book %.2f  author %.2f  genre %.2f" % tuple(np.mean(null, 0)))
        # Paul: where do the undisputed letters' chapters land at 8 groups?
        c = fcluster(L, 8, "maxclust")
        pc = Counter(c[i] for i in range(len(labs)) if A[i] == "Paul (undisputed)")
        print("Undisputed Paul's chapters spread over blind groups:", dict(pc.most_common()))
        for g, n in pc.most_common(3):
            print(f"   group {g}: {n} Paul chapters, shared with", dict(Counter(A[i] for i in range(len(labs)) if c[i]==g and A[i]!='Paul (undisputed)').most_common(4)))
