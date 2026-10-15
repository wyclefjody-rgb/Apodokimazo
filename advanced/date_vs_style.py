"""Does writing style track date? Pairwise style distance between authors vs gap in years.
Dates = rough midpoints of each author's writing career (secure, non-NT dates only)."""
import numpy as np, itertools, json
from scipy.stats import spearmanr
from common import AUTH, feats, simple, Scaler, chunk
DATE = {"Diodorus": -40, "Philo": 30, "Josephus": 85, "Appian": 150, "Justin": 155,
        "Lucian": 170, "ClementAlex": 200, "Origen": 240, "Eusebius": 320}
names = [a for a in DATE if a in AUTH]
rng = np.random.default_rng(1)
def profile(a):
    return feats(sum(AUTH[a].values(), []))
P = np.array([profile(a) for a in names])
# also chunk-level: average distance between random 1,500-word chunks
def chunks(a, n=1500, k=20):
    toks = sum(AUTH[a].values(), []); return np.array([feats(chunk(toks, n, rng)) for _ in range(k)])
C = {a: chunks(a) for a in names}
pairs = list(itertools.combinations(range(len(names)), 2))
gap = [abs(DATE[names[i]] - DATE[names[j]]) for i, j in pairs]
d_whole = [simple(P[i], P[j]) for i, j in pairs]
d_chunk = [np.mean([simple(x, y) for x in C[names[i]] for y in C[names[j]]]) for i, j in pairs]
def mantel(d, g, reps=5000):
    r = spearmanr(d, g).correlation; n = len(names); cnt = 0
    D = np.zeros((n, n)); 
    for (i, j), v in zip(pairs, d): D[i, j] = D[j, i] = v
    for _ in range(reps):
        p = rng.permutation(n); dd = [D[p[i], p[j]] for i, j in pairs]
        cnt += spearmanr(dd, g).correlation >= r
    return r, cnt / reps
out = {}
for lab, d in [("whole-author", d_whole), ("1500-word chunks", d_chunk)]:
    r, p = mantel(d, gap); out[lab] = (r, p); print(f"{lab}: Spearman r(style distance, years apart) = {r:.2f}, permutation p = {p:.2f}")
print("\nNearest author in style (whole-author profiles):")
for i, a in enumerate(names):
    ds = sorted((simple(P[i], P[j]), names[j]) for j in range(len(names)) if j != i)
    print(f"  {a:12s} ({DATE[a]:>4}) -> {ds[0][1]:12s} ({DATE[ds[0][1]]:>4}), gap {abs(DATE[a]-DATE[ds[0][1]])} yrs")
print("\nPairs sorted by style distance:")
for d, (i, j), g in sorted(zip(d_whole, pairs, gap))[:6] + [None]*0:
    print(f"  {names[i]}-{names[j]}: dist {d:.2f}, {g} yrs apart")
json.dump({"pairs": [[names[i], names[j], g, dw, dc] for (i, j), g, dw, dc in zip(pairs, gap, d_whole, d_chunk)], "mantel": out},
          open("date_vs_style.json", "w"), indent=1)
