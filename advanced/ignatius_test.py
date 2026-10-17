"""Ignatius as a control (suggested in the Discord): letters, same era, mostly accepted as one author.
Uses First1KGreek tlg1443.tlg001 (the 7 genuine letters) and tlg1443.tlg002 (long recension; we use only its
6 spurious letters, written in Ignatius's name by a later author, usually dated to the 4th century).
Usage:  py -3.12 advanced\\ignatius_test.py <tlg001.xml> <tlg002.xml>
Settings as everywhere: 100 MFW from the whole NT, Eder's Simple, Ward."""
import sys, os, itertools, numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "noise_tests"))
from extract import parts
from load import load
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
g1, g2 = sys.argv[1], sys.argv[2]
NAMES1 = {"1": "Eph", "2": "Mag", "3": "Tral", "4": "Rom", "5": "Phld", "6": "Smyr", "7": "Pol"}
SPUR = {"13": "Mary-to-Ign", "1": "To-Mary", "4": "Tarsians", "5": "Philippians", "9": "Antiochenes", "10": "Hero"}
gen = {NAMES1[n]: t for n, t in parts(g1, "epistle") if n in NAMES1}
spu = {SPUR[n]: t for n, t in parts(g2, "epistle") if n in SPUR}
print("Genuine letters (words):", {k: len(v) for k, v in gen.items()}, "total", sum(map(len, gen.values())))
print("Spurious letters (words):", {k: len(v) for k, v in spu.items()}, "total", sum(map(len, spu.values())))
ch = load("chapter"); keys = list(ch)
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
prof = lambda t: np.sqrt(np.array([Counter(t)[w] / len(t) for w in mfw]))
dist = lambda a, b: np.abs(a - b).sum()
def cut(texts, size):     # even back-to-back pieces of about `size` words (like chapters)
    out = []
    for name, t in texts.items():
        k = max(1, round(len(t) / size)); b = np.linspace(0, len(t), k + 1).astype(int)
        out += [(name, i + 1, t[b[i]:b[i + 1]]) for i in range(k)]
    return out
for size in (400, 1500):
    G = cut(gen, size); S = cut(spu, size)
    print(f"\n===== pieces of about {size} words: {len(G)} genuine, {len(S)} spurious =====")
    PG = [prof(t) for _, _, t in G]; PS = [prof(t) for _, _, t in S]
    # 1. distances: within genuine Ignatius vs within Romans chapters (same settings)
    within = np.mean([dist(a, b) for a, b in itertools.combinations(PG, 2)])
    same_letter = np.mean([dist(PG[i], PG[j]) for i, j in itertools.combinations(range(len(G)), 2) if G[i][0] == G[j][0]] or [np.nan])
    print(f"avg distance between genuine-Ignatius pieces: {within:.2f} (same letter: {same_letter:.2f})")
    # 2. single-author splitting: Ward tree of genuine pieces only, cut into 2 and 3 branches
    if len(G) >= 4:
        Z = linkage(squareform(np.array([[dist(a, b) for b in PG] for a in PG]), checks=False), "ward")
        for k in (2, 3):
            lab = fcluster(Z, k, "maxclust")
            split = sum(len(set(lab[i] for i in range(len(G)) if G[i][0] == L)) > 1 for L in gen)
            print(f"  Ward tree of genuine pieces cut into {k} branches: sizes {sorted(Counter(lab).values(), reverse=True)}; letters split across branches: {split} of 7")
    # 3. glom: genuine pieces among all 259 NT chapters + other genuine pieces
    NT = [prof(ch[k]) for k in keys]
    hit = 0
    for i, p in enumerate(PG):
        cand = [(dist(p, q), "NT") for q in NT] + [(dist(p, PG[j]), "Ign") for j in range(len(PG)) if j != i]
        hit += min(cand)[1] == "Ign"
    print(f"genuine pieces whose closest text (among 259 NT chapters + other Ignatius pieces) is Ignatius: {hit}/{len(PG)} ({hit/len(PG):.0%})")
    # 4. detection: genuine vs spurious (a known different author imitating Ignatius)
    A = PG + PS; lab = ["G"] * len(PG) + ["S"] * len(PS)
    nn = sum(lab[min((dist(A[i], A[j]), j) for j in range(len(A)) if j != i)[1]] == lab[i] for i in range(len(A)))
    Z = linkage(squareform(np.array([[dist(a, b) for b in A] for a in A]), checks=False), "ward")
    c2 = fcluster(Z, 2, "maxclust")
    tab = Counter(zip(c2, lab))
    pur = sum(max(tab[(c, "G")], tab[(c, "S")]) for c in set(c2)) / len(A)
    print(f"genuine vs spurious: pieces whose closest piece is the same group: {nn}/{len(A)} ({nn/len(A):.0%}); "
          f"2-branch Ward tree purity {pur:.0%} (branches: {dict(tab)})")
