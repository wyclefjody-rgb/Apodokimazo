"""Does keeping or removing Greek accents change the results? Same chapters, same settings (100 MFW, Eder's Simple, Ward)."""
import glob, os, re, sys, unicodedata, numpy as np
from collections import Counter, OrderedDict
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from sklearn.metrics import adjusted_rand_score as ari
KIT = sys.argv[1]
sys.path.insert(0, os.path.join(KIT, "noise_tests")); from load import GROUP
def strip(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if not unicodedata.combining(c)); return w.replace("ς", "σ")
def load(mode):
    out = OrderedDict()
    for f in sorted(glob.glob(os.path.join(KIT, "sblgnt", "*-morphgnt.txt"))):
        b = re.match(r"\d+-(\w+)-", os.path.basename(f)).group(1); b = "2-3Jn" if b in ("2Jn", "3Jn") else b
        for line in open(f, encoding="utf8"):
            ref, pos, parse, text, word, norm, lemma = line.split()
            k = b if b == "2-3Jn" else f"{b} {int(ref[2:4])}"
            w = {"accents removed (what we did)": strip(norm),
                 "accents kept, as printed": unicodedata.normalize("NFC", word.lower()),
                 "accents kept, normalised": unicodedata.normalize("NFC", norm.lower())}[mode]
            out.setdefault(k, []).append(w)
    return out
def run(ch):
    labs = list(ch); T = [ch[l] for l in labs]
    top = [w for w, _ in Counter(t for v in T for t in v).most_common(100)]
    S = np.sqrt(np.array([[Counter(v)[w] / len(v) for w in top] for v in T]))
    D = np.abs(S[:, None] - S[None]).sum(-1); np.fill_diagonal(D, np.inf)
    B = [l.split(" ")[0] for l in labs]; nn = D.argmin(1)
    L = linkage(squareform(np.where(np.isinf(D), 0, D), checks=False), "ward")
    A = [GROUP[b] for b in B]; c8 = fcluster(L, 8, "maxclust")
    acts = [i for i, b in enumerate(B) if b == "Ac"]
    return np.mean([B[i] == B[nn[i]] for i in range(len(B))]), ari(A, c8), np.mean([B[nn[i]] == "Ac" for i in acts]), top, nn, labs
base = None
for mode in ["accents removed (what we did)", "accents kept, as printed", "accents kept, normalised"]:
    nnb, a8, acts, top, nn, labs = run(load(mode))
    same = "" if base is None else f"   nearest neighbour unchanged for {np.mean(nn == base):.0%} of chapters"
    if base is None: base = nn
    print(f"{mode:32s} same-book {nnb:.0%}   author match (8 groups) {a8:.2f}   Acts->Acts {acts:.0%}{same}")
    print(f"{'':32s} top-10 words: {' '.join(top[:10])}")
