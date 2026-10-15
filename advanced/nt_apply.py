"""Step 2: apply the calibrated methods to Paul, with same-author controls and different-author comparisons.
Likelihood ratios are calibrated on the 9 undisputed Greek authors (calibrate.py) at the same sample length.
LR > 1 favours 'same author', LR < 1 favours 'different authors'; log10 LR of 1 means 10 times more likely."""
import json, numpy as np
from sklearn.linear_model import LogisticRegression
from common import AUTH, NT, OTHER, chunk, feats, Scaler, cos_sim, impostors
import calibrate as C
import sys
CAL = sys.argv[1:] or list(AUTH)      # optional: calibrate on some authors only
rng = np.random.default_rng(11)
TXT = {**NT, **OTHER}
FAM = {**{b: "Paul" for b in ["Ro","1Co","2Co","Ga","Php","1Th","Eph","Col","2Th","Pastorals"]},
       **{b: "LukeActs" for b in ["Lk","Ac","Acts1-12","Acts13-28"]}, **{b: "John" for b in ["Jn","1Jn"]}}
fam = lambda b: FAM.get(b, b)
CORE = ["Ro", "1Co", "2Co", "Ga"]
COMPS = [("Paul core letters with each other", "Paul-Paul", [(a, b) for i, a in enumerate(CORE) for b in CORE[i+1:]]),
         ("Paul core with Philippians / 1 Thessalonians", "Paul-Paul", [(a, b) for a in CORE for b in ("Php", "1Th")]),
         ("Acts 1-12 with Acts 13-28 (one author)", "control", [("Acts1-12", "Acts13-28")]),
         ("Luke with Acts (traditionally one author)", "control", [("Lk", "Ac")]),
         ("Gospel of John with 1 John (often one author)", "control", [("Jn", "1Jn")])]
for other in ["Eph","Col","Pastorals","Heb","1Pe","Jas","1Clement","Ignatius","Barnabas","Tatian","Lk","Ac","Jn","Re","Mk","Mt"]:
    COMPS.append((f"Paul core with {other}", "Paul-vs", [(a, other) for a in CORE]))
imp_texts = lambda excl: [t for a in AUTH for t in AUTH[a].values()] + [TXT[k] for k in TXT if fam(k) not in excl and k not in ("Acts1-12", "Acts13-28")]
out = {}
for n in (400, 1500):
    sc = C.pool_scaler(n)
    rows = C.pairs(n, sc, m=200, A=CAL)
    cal = {k: LogisticRegression().fit([[r[k]] for r in rows], [r["y"] for r in rows]) for k in ("cosine", "gi")}
    prior = np.log(np.mean([r["y"] for r in rows]) / (1 - np.mean([r["y"] for r in rows])))
    l10 = lambda k, s: float((cal[k].decision_function([[s]])[0] - prior) / np.log(10))
    print(f"\n=== {n}-word samples (30 random draws per comparison) ===")
    print(f"{'comparison':48s} {'median log10 LR':>16} {'draws favouring same':>21} {'impostors score':>16}")
    out[n] = {}
    for label, kind, prs in COMPS:
        lc, gi = [], []
        for d in range(30):
            a, b = prs[d % len(prs)]
            if len(TXT[a]) < n or len(TXT[b]) < n: continue
            z1, z2 = sc(np.array([feats(chunk(TXT[a], n, rng)), feats(chunk(TXT[b], n, rng))]))
            pool = imp_texts({fam(a), fam(b)})
            imp = sc(np.array([feats(chunk(pool[i], n, rng)) for i in rng.choice(len(pool), 20, replace=False)]))
            lc.append(l10("cosine", float(cos_sim(z1[None], z2[None])[0, 0]))); gi.append(impostors(z1, z2, imp, rng, k=60))
        if not lc: continue
        out[n][label] = dict(kind=kind, median_log10_lr=float(np.median(lc)), share_same=float(np.mean(np.array(lc) > 0)),
                             median_gi=float(np.median(gi)), draws=len(lc), gi=[float(x) for x in gi], log10_lr=lc)
        r = out[n][label]; print(f"{label:48s} {r['median_log10_lr']:>16.2f} {r['share_same']:>21.0%} {r['median_gi']:>16.2f}", flush=True)
    # reference: what the same statistics look like for known same/different Greek authors at this length
    for y, name in ((1, "Known Greek authors: same author, different works"), (0, "Known Greek authors: different authors")):
        v = [l10("cosine", r["cosine"]) for r in rows if r["y"] == y]; g = [r["gi"] for r in rows if r["y"] == y]
        out[n][name] = dict(kind="reference", median_log10_lr=float(np.median(v)), share_same=float(np.mean(np.array(v) > 0)), median_gi=float(np.median(g)))
        print(f"{name:48s} {np.median(v):>16.2f} {np.mean(np.array(v) > 0):>21.0%} {np.median(g):>16.2f}")
from sklearn.metrics import roc_auc_score
print("\nCan the method tell Paul-with-Paul from Paul-with-another-letter-writer (Heb, 1Pe, Jas, 1 Clement, Ignatius, Barnabas)?")
for n in out:
    pp = out[n]["Paul core letters with each other"]["gi"]
    po = sum((out[n][f"Paul core with {o}"]["gi"] for o in ["Heb","1Pe","Jas","1Clement","Ignatius","Barnabas"]), [])
    auc = roc_auc_score([1]*len(pp) + [0]*len(po), pp + po)
    out[n]["separation_auc_paul_vs_other_letters"] = float(auc)
    print(f"  {n} words: AUC {auc:.2f}  (0.5 = can't tell, 1 = always)")
json.dump(out, open("nt_results" + ("_" + "-".join(sys.argv[1:]) if sys.argv[1:] else "") + ".json", "w"), indent=1)
