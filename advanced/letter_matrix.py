"""Every letter against every other letter, one at a time (not pooled).
General Impostors score at 1,500-word samples (texts of at least 1,500 words), median of 20 random draws.
0 = never closer to each other than to other writers, 1 = always."""
import json, sys, numpy as np
from common import AUTH, NT, OTHER, chunk, feats, impostors
import calibrate as C
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
rng = np.random.default_rng(17)
TXT = {**NT, **OTHER}
ORDER = ["Ro", "1Co", "2Co", "Ga", "Php", "Eph", "Col", "Pastorals", "Heb", "1Pe", "Jas", "Acts1-12", "Acts13-28", "1Clement", "Ignatius", "Barnabas"]
NAMES = {"Ro": "Romans", "1Co": "1 Corinthians", "2Co": "2 Corinthians", "Ga": "Galatians", "Php": "Philippians", "Eph": "Ephesians", "Col": "Colossians",
         "Pastorals": "Pastorals", "Heb": "Hebrews", "1Pe": "1 Peter", "Jas": "James", "Acts1-12": "Acts 1-12", "Acts13-28": "Acts 13-28",
         "1Clement": "1 Clement", "Ignatius": "Ignatius", "Barnabas": "Barnabas"}
FAM = {**{b: "Paul" for b in ["Ro", "1Co", "2Co", "Ga", "Php", "Eph", "Col", "Pastorals"]}, "Acts1-12": "Acts", "Acts13-28": "Acts"}
fam = lambda b: FAM.get(b, b)
ORDER = [b for b in ORDER if len(TXT[b]) >= N]
sc = C.pool_scaler(N)
def pool_for(a, b):   # impostors: the 9 Greek authors + early Christian texts outside both families
    return [t for au in AUTH for t in AUTH[au].values()] + [TXT[k] for k in TXT if fam(k) not in (fam(a), fam(b)) and k not in ORDER[:0]]
M = np.full((len(ORDER), len(ORDER)), np.nan)
for i, a in enumerate(ORDER):
    for j, b in enumerate(ORDER):
        if j <= i: continue
        pool = pool_for(a, b); s = []
        for d in range(20):
            z1, z2 = sc(np.array([feats(chunk(TXT[a], N, rng)), feats(chunk(TXT[b], N, rng))]))
            imp = sc(np.array([feats(chunk(pool[k], N, rng)) for k in rng.choice(len(pool), 20, replace=False)]))
            s.append(impostors(z1, z2, imp, rng, k=60))
        M[i, j] = M[j, i] = np.median(s)
    print(f"{NAMES[a]:14s} done", flush=True)
json.dump({"order": ORDER, "names": [NAMES[b] for b in ORDER], "matrix": np.nan_to_num(M, nan=-1).tolist(), "words": N}, open(f"letter_matrix_{N}.json", "w"))
w = max(len(NAMES[b]) for b in ORDER)
print("\n" + " " * (w + 1) + " ".join(f"{NAMES[b][:5]:>5}" for b in ORDER))
for i, a in enumerate(ORDER):
    print(f"{NAMES[a]:{w}s} " + " ".join("    -" if i == j else f"{M[i, j]:5.2f}" for j in range(len(ORDER))))
