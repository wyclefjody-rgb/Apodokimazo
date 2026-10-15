import glob, os, json, numpy as np, sys
from collections import Counter
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform
sys.path.insert(0, "."); sys.path.insert(0, "../noise_tests")
from load import load as nt_load
from extract import load as tload
rng = np.random.default_rng(21)
def read(folder): return {os.path.basename(f)[:-4]: open(f, encoding="utf8").read().split() for f in sorted(glob.glob(f"{folder}/*.txt"))}
_cache = {}
def counts(v):
    k = id(v)
    if k not in _cache: _cache[k] = (Counter(v), len(v), v)
    return _cache[k]
def dist(texts, kind="delta", n=100):
    cs = [counts(v) for v in texts]
    tot = Counter()
    for c, _, _ in cs: tot.update(c)
    top = [w for w, _ in tot.most_common(n)]
    X = np.array([[c[w] / L for w in top] for c, L, _ in cs])
    if kind == "simple":
        S = np.sqrt(X); return np.abs(S[:, None] - S[None]).sum(-1)
    Z = (X - X.mean(0)) / (X.std(0) + 1e-12); m = len(top); w = (m - np.arange(1, m + 1) + 1) / m
    return (np.abs(Z[:, None] - Z[None]) * w).sum(-1) / m
def clades(D):
    Dz = D.copy(); np.fill_diagonal(Dz, 0); root = to_tree(linkage(squareform(Dz, checks=False), "ward")); out = set()
    def walk(nd):
        out.add(frozenset(nd.pre_order()))
        if not nd.is_leaf(): walk(nd.left); walk(nd.right)
    walk(root); return out
def own_branch(labels, D, group):
    idx = frozenset(i for i, l in enumerate(labels) if l.split("_")[0] == group); return idx in clades(D)
def nn_same(labels, D, group):
    D = D.copy(); np.fill_diagonal(D, np.inf); nn = D.argmin(1)
    idx = [i for i, l in enumerate(labels) if l.split("_")[0] == group]
    return np.mean([labels[nn[i]].split("_")[0] == group for i in idx])
R = {}
demo = read("corpus_their_demo"); labs = list(demo)
authors = sorted({l.split("_")[0] for l in labs})
for kind in ["delta", "simple"]:
    D = dist([demo[l] for l in labs], kind)
    R[f"their_demo_{kind}"] = {a: own_branch(labs, D, a) for a in authors}
print("1. Their demo, as they built it: each author on their own branch?")
for k, v in R.items(): print("  ", k, "all authors separate:", all(v.values()), "| Matthew:", v["Matthew"], "| 1Timothy:", v["1Timothy"], "| failed:", [a for a, ok in v.items() if not ok])

# 2. Fair version: same classical/patristic texts, but NT chapters that are NOT back-to-back, plus other NT books as competitors
nt = nt_load("chapter")
base = {k: v for k, v in demo.items() if not k.startswith(("Matthew", "1Timothy"))}
chapters = lambda b: sorted(int(l.split()[1]) for l in nt if l.split()[0] == b)
def fair_trial(kind, adjacent):
    t = dict(base); labels_nt = []
    for b, name in [("Mt", "Matthew"), ("1Ti", "1Timothy"), ("Mk", "Mark"), ("Lk", "Luke"), ("Ro", "Romans"), ("1Co", "1Corinthians")]:
        cs = chapters(b)
        if adjacent:
            s = rng.integers(cs[0], cs[-1] - 1); pick = [s, s + 1, s + 2]
        else:
            pick = sorted(rng.choice(cs, 3, replace=False))
        for c in pick: t[f"{name}_{c}"] = nt[f"{b} {c}"]
    labs = list(t); D = dist([t[l] for l in labs], kind)
    return {g: (own_branch(labs, D, g), nn_same(labs, D, g)) for g in ["Matthew", "1Timothy", "Mark", "Luke", "Romans", "1Corinthians"]}
for kind in ["delta", "simple"]:
    for adj in [True, False]:
        runs = [fair_trial(kind, adj) for _ in range(100)]
        g = runs[0].keys()
        R[f"fair_{kind}_{'adjacent' if adj else 'random'}"] = {x: {"own_branch": round(float(np.mean([r[x][0] for r in runs])), 2),
                                                               "closest_same_book": round(float(np.mean([r[x][1] for r in runs])), 2)} for x in g}
print("\n2. Same setup with 6 New Testament books (3 chapters each), 100 runs: share of runs where the book's 3 chapters form their own branch")
for k, v in R.items():
    if k.startswith("fair"): print("  ", k, {x: y["own_branch"] for x, y in v.items()})

# 3. Exhibit 6, and a single-author control: Justin's Dialogue cut into 1 Clement-sized blocks
ex = read("corpus_exhibit6")
dial = ex.pop("Justin_DialogueTrypho")
blocks = [dial[i:i + 560] for i in range(0, 13 * 560, 560)]
ex_ctrl = {k: v for k, v in ex.items()}
for i, b in enumerate(blocks): ex_ctrl[f"JustinDialogue_{i+1}"] = b
labs = list(ex_ctrl); D = dist([ex_ctrl[l] for l in labs], "delta")
def n_branches(prefix, k=8):
    from scipy.cluster.hierarchy import fcluster
    Dz = D.copy(); np.fill_diagonal(Dz, 0); c = fcluster(linkage(squareform(Dz, checks=False), "ward"), k, "maxclust")
    return len({c[i] for i, l in enumerate(labs) if l.startswith(prefix)})
R["exhibit6_control"] = {"1Clement_blocks_spread_over_branches": n_branches("1Clement_"), "JustinDialogue_blocks_spread_over_branches": n_branches("JustinDialogue_"),
                          "Barnabas_blocks_spread_over_branches": n_branches("Barnabas_"),
                          "1Clement_own_branch": own_branch(labs, D, "1Clement"), "JustinDialogue_own_branch": own_branch(labs, D, "JustinDialogue"),
                          "1Clement_closest_same": round(float(nn_same(labs, D, "1Clement")), 2), "JustinDialogue_closest_same": round(float(nn_same(labs, D, "JustinDialogue")), 2)}
print("\n3. Exhibit 6 with a single-author control (13 blocks of Justin's Dialogue, 560 words each, like 1 Clement's blocks):", R["exhibit6_control"])
Dn = D.copy(); np.fill_diagonal(Dn, np.inf)
for l in ["Revelation_1", "Revelation_2-3", "Mark_13", "Hebrews", "James", "Polycarp_Epistle", "Barnabas_16-21"]:
    i = labs.index(l); print(f"   {l:18s} closest: {[labs[j] for j in np.argsort(Dn[i])[:3]]}")
json.dump(R, open("greekdemo_results.json", "w", encoding="utf8"), indent=1, default=str)
