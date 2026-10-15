r"""Letter test: how often does each method name the right writer of a passage from LETTERS, by passage length?
Writers: Basil, Libanius, Julian, Ignatius and Pseudo-Ignatius (the later writer who forged letters in Ignatius's
name), built by build_letters.py from letters not in dispute. Chance = 1 in 5 = 20%.
As in calibrate.py, every test passage comes from a group of letters held out of that writer's reference.
  book method = 100 most frequent words of this letter collection, Eder's Simple, nearest writer
  cosine      = 800 features (300 words + 500 letter trigrams, the fixed list from common.py), z-scored, nearest centroid
  classifier  = logistic regression on the same 800 features
A writer is tested at a length only if one of its letter groups is at least that long (column "writers").

Run:            py -3.12 advanced\letters_test.py         (one run, seed 13)
Several seeds:  py -3.12 advanced\letters_test.py 100     (100 runs with seeds 13..112, spread over your CPU cores)"""
import json, os, numpy as np
from collections import Counter
from sklearn.linear_model import LogisticRegression
from common import chunk, feats, Scaler, cos_sim

HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "letters_reference.json"), encoding="utf8"))["authors"]
A = list(L); SIZES = [250, 400, 700, 1000, 1500]
pool = Counter(w for a in A for t in L[a].values() for w in t)
MFW = [w for w, _ in pool.most_common(100)]          # the book's way: most frequent words of the collection itself

def prof(tokens):
    """Eder's Simple profile: square-rooted share of each of the 100 most frequent words."""
    c = Counter(tokens); n = len(tokens)
    return np.sqrt(np.array([c[w] / n for w in MFW]))

def run(seed):
    """One full experiment; returns {length: {method: share correct, 'writers': number tested}}."""
    rng = np.random.default_rng(seed); out = {}
    for n in SIZES:
        sc = Scaler(np.array([feats(chunk(t, n, rng)) for a in A for t in L[a].values() for rep in range(4)]))
        testable = [a for a in A if any(len(t) >= n for t in L[a].values())]
        ok = {"book": [], "cosine": [], "classifier": []}
        for trial in range(15):
            # hold out one letter group per writer (long enough to give an n-word passage)
            held = {a: rng.choice([w for w, t in L[a].items() if len(t) >= n]) if a in testable else rng.choice(list(L[a]))
                    for a in A}
            RX, RY, ref = [], [], {}
            for a in A:
                works = [w for w in L[a] if w != held[a]]
                for rep in range(25):
                    RX.append(feats(chunk(L[a][rng.choice(works)], n, rng))); RY.append(a)
                ref[a] = prof(sum((L[a][w] for w in works), []))
            RZ = sc(np.array(RX))
            cent = {a: RZ[[i for i, y in enumerate(RY) if y == a]].mean(0) for a in A}
            clf = LogisticRegression(C=0.1, max_iter=2000).fit(RZ, RY)
            for a in testable:
                for rep in range(2):
                    t = chunk(L[a][held[a]], n, rng); z = sc(feats(t)[None])[0]
                    ok["book"].append(min(A, key=lambda b: np.abs(prof(t) - ref[b]).sum()) == a)
                    ok["cosine"].append(max(A, key=lambda b: cos_sim(z[None], cent[b][None])[0, 0]) == a)
                    ok["classifier"].append(clf.predict(z[None])[0] == a)
        out[n] = {k: float(np.mean(v)) for k, v in ok.items()}; out[n]["writers"] = len(testable)
    return out

def cell(v):
    """'64%' for one run, or 'average (lowest-highest)' for several."""
    return f"{v[0]:.0%}" if len(v) == 1 else f"{np.mean(v):.0%} ({min(v):.0%}-{max(v):.0%})"

if __name__ == "__main__":
    import sys
    from concurrent.futures import ProcessPoolExecutor
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print("Writers:", {a: sum(map(len, L[a].values())) for a in A}, "(words)")
    if N == 1:
        runs = [run(13)]
    else:
        with ProcessPoolExecutor() as ex:
            runs = []
            for i, r in enumerate(ex.map(run, range(13, 13 + N))):
                runs.append(r); print(f"   run {i + 1}/{N} done (seed {13 + i})", flush=True)
        print(f"\nAverage over {N} seeds, with lowest-highest in brackets:")
    w = 7 if N == 1 else 17
    print(f"Which writer wrote a passage from letters the method has never seen? (chance 1 in {len(A)})")
    print(f"{'words':>6} {'writers':>8} {'book method':>{w + 5}} {'cosine':>{w + 5}} {'classifier':>{w + 5}}")
    for n in SIZES:
        print(f"{n:>6} {runs[0][n]['writers']:>8} " + " ".join(f"{cell([r[n][k] for r in runs]):>{w + 5}}"
                                                       for k in ("book", "cosine", "classifier")))
    name = "letters_results" + ("" if N == 1 else f"_{N}seeds") + ".json"
    json.dump(runs[0] if N == 1 else {"seeds": list(range(13, 13 + N)), "runs": runs},
              open(os.path.join(HERE, name), "w"), indent=1)
