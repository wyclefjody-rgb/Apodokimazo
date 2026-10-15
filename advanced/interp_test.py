"""Interpolation sensitivity test: rerun the letter-by-letter Paul comparison with proposed
interpolations removed, and log exactly what was removed.
Tier A = text as printed (SBLGNT). Tier B = remove passages with MANUSCRIPT evidence.
Tier C = also remove passages proposed on internal grounds only (style/content), a stricter check."""
import glob, os, re, json, numpy as np
from common import AUTH, OTHER, NT, chunk, feats, impostors
from load import strip, SRC
import calibrate as C
TEXTUAL = [("Ro", 16, 25, 16, 27, "doxology moves around / missing in manuscripts"),
           ("1Co", 14, 34, 14, 35, "placed after v.40 in Western manuscripts")]
INTERNAL = [("1Th", 2, 13, 2, 16, "proposed on content grounds, no manuscript support"),
            ("2Co", 6, 14, 7, 1, "proposed on vocabulary grounds, no manuscript support"),
            ("1Co", 11, 3, 11, 16, "proposed by a minority, no manuscript support"),
            ("Ro", 13, 1, 13, 7, "proposed by a minority, no manuscript support")]
BOOKS = ["Ro", "1Co", "2Co", "Ga", "Php", "1Th"]
def verses():
    out = {}
    for f in sorted(glob.glob(f"{SRC}/*-morphgnt.txt")):
        b = re.match(r"\d+-(\w+)-", os.path.basename(f)).group(1)
        if b not in BOOKS: continue
        for line in open(f, encoding="utf8"):
            ref, *_, norm, lemma = line.split()
            out.setdefault(b, []).append(((int(ref[2:4]), int(ref[4:6])), strip(norm)))
    return out
V = verses()
def build(remove):
    txt, log = {}, []
    for b, vs in V.items():
        keep = []
        for (c, v), w in vs:
            hit = [r for r in remove if r[0] == b and (r[1], r[2]) <= (c, v) <= (r[3], r[4])]
            if not hit: keep.append(w)
        txt[b] = keep
    for r in remove:
        n = sum(1 for (c, v), w in V[r[0]] if (r[1], r[2]) <= (c, v) <= (r[3], r[4]))
        log.append({"passage": f"{r[0]} {r[1]}:{r[2]}-{r[3]}:{r[4]}", "words": n, "reason": r[5]})
    return txt, log
N, DRAWS = 1500, 40
sc = C.pool_scaler(N)
# impostors: 9 Greek authors + early Christian texts + non-Pauline NT (same idea as letter_matrix.py)
pool = [t for au in AUTH for t in AUTH[au].values()] + [OTHER[k] for k in OTHER] + \
       [NT[k] for k in ["Mt", "Mk", "Lk", "Jn", "Ac", "Heb", "Jas", "1Pe", "1Jn", "Re"]]
CORE = ["Ro", "1Co", "2Co", "Ga", "Php"]
res = {}
for tier, rem in [("A as printed", []), ("B manuscript-evidence removed", TEXTUAL), ("C all proposed removed", TEXTUAL + INTERNAL)]:
    txt, log = build(rem)
    rng = np.random.default_rng(17); out = {}
    for i, a in enumerate(CORE):
        for b in CORE[i + 1:]:
            s = []
            for _ in range(DRAWS):
                z1, z2 = sc(np.array([feats(chunk(txt[a], N, rng)), feats(chunk(txt[b], N, rng))]))
                imp = sc(np.array([feats(chunk(pool[k], N, rng)) for k in rng.choice(len(pool), 20, replace=False)]))
                s.append(impostors(z1, z2, imp, rng, k=60))
            out[f"{a}-{b}"] = float(np.median(s))
    res[tier] = {"removed": log, "words_removed": sum(l["words"] for l in log),
                 "book_words": {b: len(t) for b, t in txt.items()}, "scores": out}
    print(f"\n{tier}: removed {res[tier]['words_removed']} words")
    for l in log: print(f"   - {l['passage']:16s} {l['words']:4d} words  ({l['reason']})")
pairs = list(res["A as printed"]["scores"])
print(f"\n{'pair':10s} {'A':>6s} {'B':>6s} {'C':>6s}")
for p in pairs: print(f"{p:10s} " + " ".join(f"{res[t]['scores'][p]:6.2f}" for t in res))
json.dump(res, open("interp_test.json", "w"), indent=1)
