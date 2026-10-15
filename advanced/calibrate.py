"""Step 1: measure each method's error rate on 9 Greek authors whose authorship is not in dispute.
Every test sample comes from a work that is held out of the reference material, so a method can't win by
recognizing a book's topic or characters.
 A. Attribution (which of 9 authors wrote this sample?), chance = 11%:
      simple      = the book's method: 100 MFW, Eder's Simple, nearest author
      cosine      = 800 features (300 words + 500 letter-trigrams), z-scored, cosine to nearest author centroid
      classifier  = logistic regression trained on the same 800 features
 B. Verification (same author or not?) on pairs of samples from DIFFERENT works:
      AUC (0.5 = coin flip, 1 = perfect) for Simple distance, cosine, and General Impostors;
      then likelihood ratios calibrated by logistic regression, with Cllr (0 = perfect, 1 = uninformative),
      fitted on half the authors and tested on the other half."""
import json, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from common import AUTH, chunk, feats, simple, Scaler, cos_sim, impostors, NT, OTHER
rng = np.random.default_rng(7)
A = list(AUTH); SIZES = [250, 400, 700, 1000, 1500, 2500]
res = {"attribution": {}, "verification": {}}

def pool_scaler(n):
    X = [feats(chunk(t, n, rng)) for a in A for t in AUTH[a].values() for _ in range(4)]
    X += [feats(chunk(t, n, rng)) for t in list(NT.values()) + list(OTHER.values()) for _ in range(2)]
    return Scaler(np.array(X))

def pairs(n, sc, m=120, A=A):
    out = []
    for _ in range(m):     # same author, different works
        a = rng.choice([a for a in A if len(AUTH[a]) > 1]); w1, w2 = rng.choice(list(AUTH[a]), 2, replace=False)
        out.append((a, a, AUTH[a][w1], AUTH[a][w2], 1))
    for _ in range(m):     # different authors
        a, b = rng.choice(A, 2, replace=False)
        out.append((a, b, AUTH[a][rng.choice(list(AUTH[a]))], AUTH[b][rng.choice(list(AUTH[b]))], 0))
    rows = []
    for a, b, t1, t2, y in out:
        x1, x2 = feats(chunk(t1, n, rng)), feats(chunk(t2, n, rng)); z1, z2 = sc(x1[None])[0], sc(x2[None])[0]
        pool = [c for c in list(AUTH) if c not in (a, b)]
        imp = sc(np.array([feats(chunk(AUTH[c][rng.choice(list(AUTH[c]))], n, rng)) for c in rng.choice(pool, 20)]))
        rows.append(dict(a=a, b=b, y=y, simple=-simple(x1, x2), cosine=float(cos_sim(z1[None], z2[None])[0, 0]),
                         gi=impostors(z1, z2, imp, rng, k=60)))
    return rows
def cllr(llr, y):
    llr, y = np.asarray(llr), np.asarray(y)          # natural-log LRs
    return 0.5 * (np.mean(np.log2(1 + np.exp(-llr[y == 1]))) + np.mean(np.log2(1 + np.exp(llr[y == 0]))))
def calib(rows, key, A=A):
    """Logistic-regression calibration of scores into log-LRs, fitted on one half of the authors, tested on the other."""
    half = set(A[::2]); llr, ys = [], []
    for fit_side in (True, False):
        tr = [r for r in rows if (r["a"] in half and r["b"] in half) == fit_side]
        te = [r for r in rows if not ((r["a"] in half and r["b"] in half) == fit_side) and ((r["a"] in half) != fit_side and (r["b"] in half) != fit_side)]
        m = LogisticRegression().fit([[r[key]] for r in tr], [r["y"] for r in tr])
        prior = np.log(np.mean([r["y"] for r in tr]) / (1 - np.mean([r["y"] for r in tr])))
        llr += list(m.decision_function([[r[key]] for r in te]) - prior); ys += [r["y"] for r in te]
    return cllr(llr, ys), llr, ys

if __name__ == "__main__":
    import sys
    SUB = sys.argv[1:]            # optional: restrict to some authors, e.g. the Christian and Jewish writers
    if SUB: A = SUB
    print(f"Authors: {A}")
    print("A. Attribution: which author wrote a sample from a work the method has never seen (chance 1 in " + str(len(A)) + ")")
    print(f"{'words':>6} {'book method':>12} {'cosine':>8} {'classifier':>11}")
    for n in SIZES:
        sc = pool_scaler(n); ok = {"simple": [], "cosine": [], "classifier": []}
        for trial in range(15):
            held = {a: rng.choice(list(AUTH[a])) for a in A}
            # reference: 25 samples per author from its other works
            RX, RY, prof = [], [], {}
            for a in A:
                works = [w for w in AUTH[a] if w != held[a]]
                for _ in range(25):
                    RX.append(feats(chunk(AUTH[a][rng.choice(works)], n, rng))); RY.append(a)
                prof[a] = feats(sum((AUTH[a][w] for w in works), []))
            RX = np.array(RX); RZ = sc(RX)
            cent = {a: RZ[[i for i, y in enumerate(RY) if y == a]].mean(0) for a in A}
            clf = LogisticRegression(C=0.1, max_iter=2000).fit(RZ, RY)
            for a in A:
                for _ in range(2):
                    x = feats(chunk(AUTH[a][held[a]], n, rng)); z = sc(x[None])[0]
                    ok["simple"].append(min(A, key=lambda b: simple(x, prof[b])) == a)
                    ok["cosine"].append(max(A, key=lambda b: cos_sim(z[None], cent[b][None])[0, 0]) == a)
                    ok["classifier"].append(clf.predict(z[None])[0] == a)
        res["attribution"][n] = {k: float(np.mean(v)) for k, v in ok.items()}
        r = res["attribution"][n]; print(f"{n:>6} {r['simple']:>12.0%} {r['cosine']:>8.0%} {r['classifier']:>11.0%}", flush=True)
    
    print("\nB. Verification: are two samples (from different works) by the same author?")
    print(f"{'words':>6} {'AUC simple':>11} {'AUC cosine':>11} {'AUC impostors':>14} {'Cllr cosine':>12} {'Cllr impostors':>15}")
    for n in (400, 700, 1500, 2500):
        sc = pool_scaler(n); rows = pairs(n, sc, A=A); y = [r["y"] for r in rows]
        auc = {k: roc_auc_score(y, [r[k] for r in rows]) for k in ("simple", "cosine", "gi")}
        cc, llr_c, yc = calib(rows, "cosine", A=A); cg, llr_g, yg = calib(rows, "gi", A=A)
        res["verification"][n] = dict(auc=auc, cllr_cosine=cc, cllr_gi=cg,
            median_log10_lr_same=float(np.median(np.array(llr_c)[np.array(yc) == 1]) / np.log(10)),
            median_log10_lr_diff=float(np.median(np.array(llr_c)[np.array(yc) == 0]) / np.log(10)), n_pairs=len(rows))
        print(f"{n:>6} {auc['simple']:>11.2f} {auc['cosine']:>11.2f} {auc['gi']:>14.2f} {cc:>12.2f} {cg:>15.2f}", flush=True)
    json.dump(res, open("calibration_results" + ("_" + "-".join(SUB) if SUB else "") + ".json", "w"), indent=1)
