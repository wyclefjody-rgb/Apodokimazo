"""Reconstruct the Stylo-default pipeline and stress-test it."""
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import json, random
import numpy as np
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import adjusted_rand_score
from load import load, book_of, GROUP

rng = np.random.default_rng(0)
random.seed(0)
R = {}


def freq_matrix(texts, n_mfw, vocab=None):
    labels = list(texts)
    if vocab is None:
        tot = Counter(t for toks in texts.values() for t in toks)
        vocab = [w for w, _ in tot.most_common(n_mfw)]
    idx = {w: i for i, w in enumerate(vocab)}
    X = np.zeros((len(labels), len(vocab)))
    for r, l in enumerate(labels):
        c = Counter(texts[l])
        n = len(texts[l])
        for w, k in c.items():
            if w in idx:
                X[r, idx[w]] = k / n
    return labels, X, vocab


def delta(X, kind="classic"):
    Z = (X - X.mean(0)) / (X.std(0) + 1e-12)
    if kind == "classic":
        return pdist(Z, "cityblock") / X.shape[1]
    if kind == "cosine":
        return pdist(Z, "cosine")
    if kind == "simple":  # Eder's Simple: Manhattan on square-rooted relative frequencies
        return pdist(np.sqrt(X), "cityblock")
    if kind == "eder":
        return pdist(Z, "euclidean")


import os
DIST=os.environ.get("DIST","simple")
def cluster(texts, n_mfw=100, dist=DIST, link="ward", vocab=None):
    labels, X, vocab = freq_matrix(texts, n_mfw, vocab)
    D = delta(X, dist)
    L = linkage(D, method=link)
    return labels, D, L


def nn_same(labels, D, key=book_of):
    M = squareform(D)
    np.fill_diagonal(M, np.inf)
    nn = M.argmin(1)
    return np.mean([key(labels[i]) == key(labels[j]) for i, j in enumerate(nn)])


grp = lambda l: GROUP[book_of(l)]

# ---------- A. reproduction ----------
ch = load("chapter")
lens = np.array([len(v) for v in ch.values()])
R["n_chapters"] = len(ch)
R["chapter_len"] = {"median": int(np.median(lens)), "p10": int(np.percentile(lens, 10)),
                    "p90": int(np.percentile(lens, 90)), "min": int(lens.min()),
                    "share_under_1000": float((lens < 1000).mean()),
                    "share_under_2500": float((lens < 2500).mean())}
labels, D, L = cluster(ch)
R["base_nn_same_book"] = nn_same(labels, D)
R["base_nn_same_group"] = nn_same(labels, D, grp)
dn = dendrogram(L, labels=labels, no_plot=True)
R["base_leaf_order"] = dn["ivl"]

json.dump(labels, open("labels.json", "w", encoding="utf8"))

# ---------- B. stability across reasonable settings ----------
K = 27  # roughly one cluster per book
settings = [(m, d, l) for m in (50, 100, 200, 300, 500)
            for d in ("classic", "cosine", "simple") for l in ("ward", "average", "complete")]
parts = {}
for m, d, l in settings:
    lab, Dm, Lm = cluster(ch, m, d, l)
    parts[(m, d, l)] = fcluster(Lm, K, "maxclust")
base = parts[(100, DIST, "ward")]
R["stability_ari_vs_default"] = {f"{m}|{d}|{l}": float(adjusted_rand_score(base, p))
                                 for (m, d, l), p in parts.items()}
# co-clustering: for each chapter pair, fraction of runs placing them together
P = np.array(list(parts.values()))
co = np.zeros((len(labels), len(labels)))
for p in P:
    co += (p[:, None] == p[None, :])
co /= len(P)
iu = np.triu_indices(len(labels), 1)
cv = co[iu]
R["pairs_ever_together"] = int((cv > 0).sum())
R["pairs_always_together"] = int((cv == 1).sum())
R["pairs_together_in_default"] = int((base[:, None] == base[None, :])[iu].sum())
dt = (base[:, None] == base[None, :])[iu]
R["default_pairs_that_survive_75pct"] = float((cv[dt] >= .75).mean())
# chapter-level instability: how many different nearest neighbours does each chapter get?
nns = []
for m, d, l in settings:
    lab, X, _ = freq_matrix(ch, m)
    M = squareform(delta(X, d)); np.fill_diagonal(M, np.inf)
    nns.append(M.argmin(1))
nns = np.array(nns)
n_distinct = [len(set(nns[:, i])) for i in range(len(labels))]
R["nn_distinct_mean"] = float(np.mean(n_distinct))
R["nn_changes_share"] = float(np.mean([x > 1 for x in n_distinct]))

# ---------- C. chunk size vs. self-attribution (the key noise test) ----------
bk = load("book")
sizes = [150, 300, 500, 750, 1000, 1500, 2000, 3000, 5000]
curve = []
for S in sizes:
    for n_mfw in (100,):
        accs, accs_g = [], []
        for rep in range(5):
            chunks = {}
            for b, toks in bk.items():
                off = rng.integers(0, S) if len(toks) > 2 * S else 0
                toks2 = toks[off:]
                for i in range(len(toks2) // S):
                    chunks[f"{b} #{i}"] = toks2[i * S:(i + 1) * S]
            # only score chunks whose book has >=2 chunks (so a same-book neighbour exists)
            lab, X, _ = freq_matrix(chunks, n_mfw)
            M = squareform(delta(X, DIST)); np.fill_diagonal(M, np.inf)
            # exclude adjacent chunks (i±1) so contiguous-topic overlap can't carry the result
            for i, l in enumerate(lab):
                b, k = l.split(" #"); k = int(k)
                for j, l2 in enumerate(lab):
                    b2, k2 = l2.split(" #")
                    if b2 == b and abs(int(k2) - k) == 1:
                        M[i, j] = np.inf
            cnt = Counter(book_of(l) for l in lab)
            ok = [i for i, l in enumerate(lab) if cnt[book_of(l)] >= 3]
            nn = M.argmin(1)
            accs.append(np.mean([book_of(lab[i]) == book_of(lab[nn[i]]) for i in ok]))
            accs_g.append(np.mean([grp(lab[i]) == grp(lab[nn[i]]) for i in ok]))
        curve.append({"size": S, "same_book": float(np.mean(accs)), "same_group": float(np.mean(accs_g)),
                      "n_chunks": len(lab)})
R["chunk_curve"] = curve

# ---------- D. null test: shuffled text still yields a confident-looking tree ----------
alltoks = [t for v in ch.values() for t in v]
null_nn, null_heights, real_heights = [], [], sorted(L[:, 2])[-10:]
for rep in range(20):
    perm = rng.permutation(alltoks)
    fake, p = {}, 0
    for l, v in ch.items():
        fake[l] = list(perm[p:p + len(v)]); p += len(v)
    labf, Df, Lf = cluster(fake)
    null_nn.append(nn_same(labf, Df))
R["null_nn_same_book_mean"] = float(np.mean(null_nn))
R["null_nn_same_book_max"] = float(np.max(null_nn))
# expected by chance given book sizes
cnt = Counter(book_of(l) for l in labels)
R["chance_same_book"] = float(sum(c * (c - 1) for c in cnt.values()) / (len(labels) * (len(labels) - 1)))
# save a null linkage for plotting
np.save("null_linkage.npy", Lf)

# ---------- E. one-author control: Acts alone ----------
acts = {l: v for l, v in ch.items() if book_of(l) == "Ac"}
la, Da, La = cluster(acts)
for k in (2, 3, 4):
    R[f"acts_split_k{k}"] = {int(c): [l for l, cc in zip(la, fcluster(La, k, "maxclust")) if cc == c]
                             for c in set(fcluster(La, k, "maxclust"))}
# Acts: narrative chapters vs speech-heavy chapters
# Luke-Acts together: do Luke & Acts chapters mix, or separate by genre/section?
la2 = {l: v for l, v in ch.items() if book_of(l) in ("Lk", "Ac")}
lb, Db, Lb = cluster(la2)
cb = fcluster(Lb, 2, "maxclust")
R["luke_acts_k2"] = {int(c): Counter(book_of(l) for l, cc in zip(lb, cb) if cc == c) for c in set(cb)}

# ---------- F. topic leakage: function-words only vs. MFW ----------
import glob, os
FW_POS = {"RA", "C-", "X-", "P-", "RP", "RR", "RD", "RI", "RE", "RD"}
fw = set()
for f in glob.glob(os.path.join(os.environ.get("SBLGNT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sblgnt")), "*-morphgnt.txt")):
    for line in open(f, encoding="utf8"):
        parts_ = line.split()
        if parts_[1] in FW_POS:
            from load import strip
            fw.add(strip(parts_[5]))
tot = Counter(t for v in ch.values() for t in v)
mfw100 = [w for w, _ in tot.most_common(100)]
R["mfw100_non_function"] = [w for w in mfw100 if w not in fw]
R["mfw100_non_function_n"] = len(R["mfw100_non_function"])
fw_vocab = [w for w, _ in tot.most_common() if w in fw][:100]
lf_, Dfw, Lfw = cluster(ch, vocab=fw_vocab)
R["fw_nn_same_book"] = nn_same(lf_, Dfw)
R["fw_nn_same_group"] = nn_same(lf_, Dfw, grp)

json.dump(R, open(f"results_{DIST}.json", "w", encoding="utf8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items() if k not in ("base_leaf_order", "stability_ari_vs_default")},
                 ensure_ascii=False, indent=1, default=str))
a = R["stability_ari_vs_default"]
print("ARI vs default: min %.2f median %.2f" % (min(a.values()), np.median(list(a.values()))))
