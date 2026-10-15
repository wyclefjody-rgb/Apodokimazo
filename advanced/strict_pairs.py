"""Stricter impostor test: the 'impostors' now include Paul's own other letters too.
For A vs B to score high, B must look more like A than Romans, 1-2 Corinthians and Galatians do (and more than other writers)."""
import numpy as np
from common import AUTH, NT, OTHER, chunk, feats, impostors
import calibrate as C
N = 1500; rng = np.random.default_rng(23); TXT = {**NT, **OTHER}; sc = C.pool_scaler(N)
CORE = ["Ro", "1Co", "2Co", "Ga"]
base = [t for au in AUTH for t in AUTH[au].values()] + [TXT[k] for k in ["Heb", "1Pe", "Jas", "1Clement", "Barnabas", "Tatian", "Lk", "Jn"]]
def gi(a, b, extra):
    pool = base + [TXT[k] for k in extra]; s = []
    for d in range(20):
        z1, z2 = sc(np.array([feats(chunk(TXT[a], N, rng)), feats(chunk(TXT[b], N, rng))]))
        idx = list(rng.choice(len(base), 14, replace=False)) + list(range(len(base), len(pool))) * 2   # always include the extra (Paul) impostors
        imp = sc(np.array([feats(chunk(pool[k], N, rng)) for k in idx]))
        s.append(impostors(z1, z2, imp, rng, k=60))
    return np.median(s)
tests = [("Php", "Ignatius", CORE, "Philippians vs Ignatius, with core Paul as impostors"),
         ("Php", "Ro", ["1Co", "2Co", "Ga", "Ignatius"], "Philippians vs Romans, with other Paul + Ignatius as impostors"),
         ("Php", "1Co", ["Ro", "2Co", "Ga", "Ignatius"], "Philippians vs 1 Corinthians, same"),
         ("Php", "2Co", ["Ro", "1Co", "Ga", "Ignatius"], "Philippians vs 2 Corinthians, same"),
         ("Php", "Ga", ["Ro", "1Co", "2Co", "Ignatius"], "Philippians vs Galatians, same"),
         ("Col", "Ignatius", CORE, "Colossians vs Ignatius, with core Paul as impostors"),
         ("Eph", "Ignatius", CORE, "Ephesians vs Ignatius, with core Paul as impostors")]
for a, b, extra, label in tests:
    print(f"{label:70s} {gi(a, b, extra):.2f}", flush=True)
