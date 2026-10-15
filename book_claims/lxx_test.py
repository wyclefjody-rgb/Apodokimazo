"""Their Exhibit 5 claim: Revelation 4-22 clusters with the Septuagint, so it was translated from Hebrew.
Same test on Luke 1-2, which they say the author of Acts wrote in Greek."""
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import os, csv, re, unicodedata, numpy as np, json
from collections import Counter, OrderedDict
from load import load

def norm(w):
    w = unicodedata.normalize("NFD", w.lower().replace("ϲ", "σ"))
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^α-ω]", "", w.replace("ς", "σ"))

L = os.environ.get("LXX", "../lxx") + "/"
words = [norm(r[2]) if len(r) > 2 else "" for r in csv.reader(open(L + "01_wordlist_unicode/text_koine.csv", encoding="utf8"), delimiter="\t")]
starts = [(r[0].split(".")[0], int(r[1])) for r in csv.reader(open(L + "08_versification/001_verse_c_modified_KEEP.csv", encoding="utf8"), delimiter="\t")]
lxx = OrderedDict()
for i, (bk, s) in enumerate(starts):
    e = starts[i + 1][1] if i + 1 < len(starts) else len(words) + 1
    lxx.setdefault(bk, []).extend(w for w in words[s - 1:e - 1] if w)
KEEP = ["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Esth","Jonah","Dan","Bar","Jdt","1Mac","2Mac","3Mac","4Mac","Wis","Sir","Tob","Isa","Ezek","Jer","Ps"]
lxx = {("LXX " + k): v for k, v in lxx.items() if any(k.startswith(x) for x in KEEP) and len(v) > 1500}

ch = load("chapter")
fix = lambda t: [norm(w) for w in t if norm(w)]
def join(book, a, b): return fix([w for c in range(a, b + 1) for w in ch[f"{book} {c}"]])
nt = {
 "Revelation 1": join("Re", 1, 1), "Revelation 2-3": join("Re", 2, 3), "Revelation 4-22": join("Re", 4, 22),
 "Luke 1-2": join("Lk", 1, 2), "Luke 3-24": join("Lk", 3, 24), "Acts": join("Ac", 1, 28),
 "Mark": join("Mk", 1, 16), "Matthew": join("Mt", 1, 28), "John": join("Jn", 1, 21),
 "Romans": join("Ro", 1, 16), "1 Corinthians": join("1Co", 1, 16), "Hebrews": join("Heb", 1, 13),
}
texts = {**lxx, **nt}
labs = list(texts)
tot = Counter(w for v in texts.values() for w in v)
top = [w for w, _ in tot.most_common(100)]
X = np.array([[Counter(texts[l])[w] / len(texts[l]) for w in top] for l in labs])
S = np.sqrt(X); D = np.abs(S[:, None] - S[None]).sum(-1); np.fill_diagonal(D, np.inf)
out = {}
for l in nt:
    i = labs.index(l)
    order = [labs[j] for j in np.argsort(D[i])[:3]]
    lx = min(D[i, j] for j, m in enumerate(labs) if m.startswith("LXX"))
    ntd = min(D[i, j] for j, m in enumerate(labs) if not m.startswith("LXX") and m != l)
    out[l] = {"words": len(nt[l]), "closest": order, "nearest_LXX": round(lx, 2), "nearest_NT": round(ntd, 2),
              "closer_to": "Septuagint" if lx < ntd else "New Testament"}
json.dump(out, open("lxx_results.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
for k, v in out.items(): print(f"{k:16s} {v['words']:>6} words  closer to {v['closer_to']:13s} LXX {v['nearest_LXX']:.2f} vs NT {v['nearest_NT']:.2f}  {v['closest']}")
