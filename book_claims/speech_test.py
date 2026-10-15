"""Their claim: Mark 13 (and Matt 24, Luke 21) and John 14-17 stand apart, so they had different authors.
Check: what are these chapters' closest matches? If other long speeches from other books, the grouping is genre."""
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import numpy as np, json
from collections import Counter
from load import load, book_of
ch = load("chapter"); labs = list(ch)
tot = Counter(t for v in ch.values() for t in v); top = [w for w, _ in tot.most_common(100)]
X = np.array([[Counter(ch[l])[w] / len(ch[l]) for w in top] for l in labs]); S = np.sqrt(X)
D = np.abs(S[:, None] - S[None]).sum(-1); np.fill_diagonal(D, np.inf)
# chapters that are mostly one long speech by Jesus
SPEECH = {"Mk 13", "Mt 5", "Mt 6", "Mt 7", "Mt 10", "Mt 18", "Mt 23", "Mt 24", "Mt 25", "Lk 21", "Lk 12", "Lk 15", "Lk 16",
          "Jn 14", "Jn 15", "Jn 16", "Jn 17", "Jn 10", "Jn 6"}
out = {}
for l in ["Mk 13", "Mt 24", "Lk 21", "Jn 14", "Jn 15", "Jn 16", "Jn 17"]:
    i = labs.index(l); nn = [labs[j] for j in np.argsort(D[i])[:4]]
    out[l] = nn
    print(f"{l:6s} -> {', '.join(nn)}")
# Of the speech chapters, how often is the closest match another speech chapter vs. chance?
hits = [labs[np.argmin(D[labs.index(l)])] in SPEECH for l in SPEECH]
gospel = [l for l in labs if book_of(l) in ("Mt", "Mk", "Lk", "Jn")]
chance = (len(SPEECH) - 1) / (len(gospel) - 1)
print(f"speech chapters whose closest match is another speech chapter: {np.mean(hits):.0%} (chance within the Gospels ~{chance:.0%})")
out["speech_to_speech"] = float(np.mean(hits)); out["chance"] = chance
json.dump(out, open("speech_results.json", "w", encoding="utf8"), indent=1)
