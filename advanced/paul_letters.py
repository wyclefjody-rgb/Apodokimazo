r"""Paul in the letter lineup: the letter test's setup (a passage compared with each writer's whole reference),
with Paul added as a sixth writer. Paul's reference = his six undisputed longer letters (Ro, 1Co, 2Co, Ga, Php, 1Th).
  Controls:  each undisputed letter is held out in turn; does a 400-word passage from it go to Paul?
  Tested:    disputed letters (Eph, Col, 2Th, Pastorals) and letters nobody gives to Paul (Heb, 1Pe, Jas, 1 Clement,
             Barnabas). The lineup has no 'none of these', so the useful comparison is disputed vs not-Paul letters.
  book method = 100 most frequent words of the lineup, Eder's Simple, nearest writer
  classifier  = logistic regression on the 800 fixed features from common.py
Run:  py -3.12 advanced\paul_letters.py        (seeds 31..35)     or   ... paul_letters.py 20   (seeds 31..50)"""
import json, os, sys, numpy as np
from collections import Counter, defaultdict
from sklearn.linear_model import LogisticRegression
from common import chunk, feats, Scaler, NT, OTHER

HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "letters_reference.json"), encoding="utf8"))["authors"]
PAUL = ["Ro", "1Co", "2Co", "Ga", "Php", "1Th"]
L["Paul"] = {b: NT[b] for b in PAUL}
A = list(L)
TEST = {**{b: NT[b] for b in ["Eph", "Col", "2Th", "Pastorals", "Heb", "1Pe", "Jas"]},
        "1Clement": OTHER["1Clement"], "Barnabas": OTHER["Barnabas"]}
MFW = [w for w, _ in Counter(w for a in A for t in L[a].values() for w in t).most_common(100)]
prof = lambda t: (lambda c, n: np.sqrt(np.array([c[w] / n for w in MFW])))(Counter(t), len(t))

def run(seed, n=400, per=20):
    """Share of passages attributed to each writer, for each held-out Paul letter and each tested letter."""
    rng = np.random.default_rng(seed); out = {}
    sc = Scaler(np.array([feats(chunk(t, n, rng)) for a in A for t in L[a].values() for rep in range(4)]))
    def fit(exclude=None):
        """References with one Paul letter left out (or none): Eder profiles + a classifier."""
        RX, RY, ref = [], [], {}
        for a in A:
            works = [w for w in L[a] if not (a == "Paul" and w == exclude)]
            for rep in range(25):
                RX.append(feats(chunk(L[a][rng.choice(works)], n, rng))); RY.append(a)
            ref[a] = prof(sum((L[a][w] for w in works), []))
        return ref, LogisticRegression(C=0.1, max_iter=3000).fit(sc(np.array(RX)), RY)
    def tally(text, ref, clf):
        got = {"book": Counter(), "classifier": Counter()}
        for rep in range(per):
            t = chunk(text, n, rng)
            got["book"][min(A, key=lambda b: np.abs(prof(t) - ref[b]).sum())] += 1
            got["classifier"][clf.predict(sc(feats(t)[None]))[0]] += 1
        return got
    for b in PAUL:                                   # controls: Paul's own letters, each held out
        out[b] = tally(L["Paul"][b], *fit(exclude=b))
    ref, clf = fit()
    for k, t in TEST.items():
        out[k] = tally(t, ref, clf)
    return out

if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    with ProcessPoolExecutor() as ex:
        runs = list(ex.map(run, range(31, 31 + N)))
    print(f"400-word passages, {N} runs x 20 passages per letter. Lineup: {', '.join(A)} (chance 1 in {len(A)})")
    for method in ("book", "classifier"):
        print(f"\n{method}: share of passages given to Paul (and the most common other choice)")
        for k in PAUL + list(TEST):
            tot = sum((r[k][method] for r in runs), Counter()); s = sum(tot.values())
            other = [(a, c) for a, c in tot.most_common() if a != "Paul"][:1]
            tag = "Paul, held out" if k in PAUL else ("disputed" if k in ("Eph", "Col", "2Th", "Pastorals") else "not Paul")
            print(f"  {k:10s} {tag:15s} Paul {tot['Paul'] / s:>4.0%}" + (f"   next: {other[0][0]} {other[0][1] / s:.0%}" if other else ""))
