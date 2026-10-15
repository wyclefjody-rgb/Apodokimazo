"""Their book, their method, at their Paul length. See README.md."""
import glob, os, re, shutil, sys
import numpy as np
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
HERE = os.path.dirname(os.path.abspath(__file__))
tok = lambda s: re.findall(r"[a-z]+(?:'[a-z]+)?", s.lower())
T = {os.path.basename(f)[:-4]: tok(open(f, encoding="utf8", errors="ignore").read()) for f in sorted(glob.glob(os.path.join(HERE, "texts", "*.txt")))}
if len(T) < 4: sys.exit("Put at least 4 chapter files in the texts folder first (see README.md).")
author = lambda k: k.split("_")[0]
print("Chapters:", ", ".join(f"{k} ({len(v):,} words)" for k, v in T.items()))
rng = np.random.default_rng(1)

def dist(texts):
    top = [w for w, _ in Counter(t for v in texts for t in v).most_common(100)]
    S = np.sqrt(np.array([[Counter(v)[w] / len(v) for w in top] for v in texts]))
    return np.abs(S[:, None] - S[None]).sum(-1)

def pieces(size, per=4):
    labs, txt = [], []
    for k, t in T.items():
        if size is None or len(t) <= size:
            labs.append(k); txt.append(t if size is None else t); continue
        for i, s in enumerate(sorted(rng.choice(len(t) - size, min(per, max(1, len(t) // size)), replace=False))):
            labs.append(f"{k}_{i+1}"); txt.append(t[s:s + size])
    return labs, txt

chap = lambda l: "_".join(l.split("_")[:2])
for name, size in [("whole chapters", None), ("4,000 words", 4000), ("1,500 words", 1500), ("700 words", 700), ("400 words (a Pauline chapter)", 400)]:
    accs, splits, chance = [], [], []
    for rep in range(1 if size is None else 20):
        labs, txt = pieces(size)
        D = dist(txt); np.fill_diagonal(D, np.inf)
        ok = []
        for i, l in enumerate(labs):
            d = D[i].copy()
            for j, m in enumerate(labs):
                if chap(m) == chap(l): d[j] = np.inf          # must match a DIFFERENT chapter
            ok.append(author(labs[d.argmin()]) == author(l))
        accs.append(np.mean(ok))
        A = [author(l) for l in labs]
        chance.append(np.mean([(sum(a == author(l) for a in A) - sum(chap(m) == chap(l) for m in labs)) / max(1, sum(chap(m) != chap(l) for m in labs)) for l in labs]))
        if size is not None:
            c = fcluster(linkage(squareform(np.where(np.isinf(D), 0, D), checks=False), "ward"), 2, "maxclust")
            splits.append(sum(len({c[i] for i, l in enumerate(labs) if chap(l) == k}) > 1 for k in T))
        if rep == 0:
            out = os.path.join(HERE, "corpus_" + ("whole" if size is None else str(size)))
            shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
            for l, t in zip(labs, txt): open(os.path.join(out, l + ".txt"), "w", encoding="utf8").write(" ".join(t))
    line = f"{name:32s} closest piece is by the same author: {np.mean(accs):.0%}   (chance about {np.mean(chance):.0%})"
    if splits: line += f"   chapters split across both groups: {np.mean(splits):.1f} of {len(T)}"
    print(line)
