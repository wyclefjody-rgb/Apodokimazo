import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import sys, re, glob, os, json, numpy as np
from collections import Counter
sys.path.insert(0, "noise_tests") if os.path.isdir("noise_tests") else None
from load import load, book_of
rng = np.random.default_rng(0)

def simple(texts, n=100):
    tot = Counter(t for v in texts for t in v)
    top = [w for w, _ in tot.most_common(n)]
    X = np.array([[Counter(v)[w] / len(v) for w in top] for v in texts])
    S = np.sqrt(X)
    return np.abs(S[:, None] - S[None]).sum(-1)

out = {}
# 1. Claim: English demo works on whole novels. Same novels cut to NT-chapter size.
nov = {os.path.basename(f)[:-4]: re.findall(r"[a-z']+", open(f, encoding="utf8", errors="ignore").read().lower()) for f in glob.glob("novels/*.txt")}
auth = lambda k: k.split("_")[0]
res = {}
for S in [400, 700, 2000, 5000, None]:
    accs = []
    for rep in range(30):
        labs, txt = [], []
        for k, t in nov.items():
            if S is None:
                labs.append(k); txt.append(t); continue
            for i in range(4):           # 4 random chunks per novel
                o = rng.integers(0, len(t) - S); labs.append(k); txt.append(t[o:o + S])
        D = simple(txt); np.fill_diagonal(D, np.inf)
        # correct = nearest neighbour is a DIFFERENT novel by the SAME author (true attribution test)
        ok = []
        for i in range(len(labs)):
            if auth(labs[i]) == 'EBronte': continue   # only one novel, so no other novel to match
            d = D[i].copy()
            for j in range(len(labs)):
                if labs[j] == labs[i]: d[j] = np.inf       # can't just match its own novel
            j = d.argmin(); ok.append(auth(labs[j]) == auth(labs[i]))
        accs.append(np.mean(ok))
        if S is None: break
    res[str(S or "whole novel")] = float(np.mean(accs))
out["novels_author_accuracy"] = res
out["novel_words"] = {k: len(v) for k, v in nov.items()}

# 2. Their Greek demo: Matthew 5-7 and 1 Timothy 1-3 "correctly attributed". Are adjacent chapters doing the work?
ch = load("chapter")
labs = list(ch); D = simple([ch[l] for l in labs]); np.fill_diagonal(D, np.inf)
nn = D.argmin(1)
same = [i for i in range(len(labs)) if book_of(labs[i]) == book_of(labs[nn[i]])]
def num(l): return int(l.split()[1]) if " " in l else 0
adj = [i for i in same if abs(num(labs[i]) - num(labs[nn[i]])) == 1]
out["nn_same_book"] = len(same) / len(labs)
out["same_book_matches_that_are_adjacent_chapters"] = len(adj) / len(same)
# same-book match rate once the chapter's immediate neighbours are hidden
D2 = D.copy()
for i in range(len(labs)):
    for j in range(len(labs)):
        if book_of(labs[i]) == book_of(labs[j]) and abs(num(labs[i]) - num(labs[j])) == 1: D2[i, j] = np.inf
nn2 = D2.argmin(1)
out["nn_same_book_excluding_adjacent"] = float(np.mean([book_of(labs[i]) == book_of(labs[nn2[i]]) for i in range(len(labs))]))
# Their exact demo, but with NON-adjacent chapters: 3 random chapters from Matthew and 3 from 1 Timothy vs the rest of the NT
Mt = [l for l in labs if book_of(l) == "Mt"]; Ti = [l for l in labs if book_of(l) == "1Ti"]
def cohesion(group):
    idx = [labs.index(l) for l in group]
    return np.mean([book_of(labs[nn[i]]) == book_of(labs[i]) for i in idx])
out["Mt_5_6_7_nn_same_book"] = cohesion(["Mt 5", "Mt 6", "Mt 7"])
out["1Ti_1_2_3_nn_same_book"] = cohesion(["1Ti 1", "1Ti 2", "1Ti 3"])
out["all_Matthew_chapters_nn_same_book"] = cohesion(Mt)
out["Mt_nearest"] = {l: labs[nn[labs.index(l)]] for l in Mt}
# 3. Claim: theological words don't make the top 100
tot = Counter(t for v in ch.values() for t in v)
out["top100_includes"] = [w for w in ["θεου","θεοσ","ιησουσ","ιησου","χριστου","κυριου","κυριοσ","πνευμα","υιοσ","θεω"] if w in [x for x, _ in tot.most_common(100)]]
print(json.dumps(out, ensure_ascii=False, indent=1))
