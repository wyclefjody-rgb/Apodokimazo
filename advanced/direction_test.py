"""Does 'Evangelion is closer to Luke 4-22 than to Acts / Luke 1-3 & 23-24' show which came first?
Simulate the LUKE-FIRST scenario: make a 'cut-down Luke' = Luke 4-22 with chapters 1-3, 23-24 dropped and
random verses removed (as Marcion would have cut). If this cut-down Luke shows the SAME distance pattern
Gray Eyes reports for the Evangelion, the pattern can't tell direction.
100 MFW (whole NT), Eder's Simple, whole-text profiles."""
import glob, os, re, sys, numpy as np
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load, strip, SRC
ch = load("chapter"); keys = list(ch)
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
def prof(t): c = Counter(t); return np.sqrt(np.array([c[w] / len(t) for w in mfw]))
dist = lambda a, b: np.abs(prof(a) - prof(b)).sum()
# Luke by verse
LV = []
for line in open(glob.glob(f"{SRC}/*-Lk-morphgnt.txt")[0], encoding="utf8"):
    ref, *_, norm, lemma = line.split(); LV.append(((int(ref[2:4]), int(ref[4:6])), strip(norm)))
verses = {}
for (c, v), w in LV: verses.setdefault((c, v), []).append(w)
mid = [cv for cv in verses if 4 <= cv[0] <= 22]
L422 = sum((verses[cv] for cv in mid), [])
pad = sum((verses[cv] for cv in verses if cv[0] <= 3 or cv[0] >= 23), [])
acts = sum((ch[k] for k in keys if k.startswith("Ac ")), [])
print(f"Luke 4-22: {len(L422)} words | Luke 1-3 + 23-24: {len(pad)} | Acts: {len(acts)}")
print(f"\nReference: Acts <-> Luke 1-3+23-24 ('padding') = {dist(acts, pad):.3f}")
rng = np.random.default_rng(3)
for frac in (0.15, 0.30):
    res = []
    for _ in range(50):
        keep = [cv for cv in mid if rng.random() > frac]
        cut = sum((verses[cv] for cv in keep), [])
        # compare the cut text with the FULL Luke 4-22 it was cut from, with Acts, and with the padding
        res.append((dist(cut, L422), dist(cut, acts), dist(cut, pad)))
    r = np.array(res).mean(0)
    print(f"\nCut-down Luke (1-3 & 23-24 gone, {int(frac*100)}% of 4-22 verses removed at random), avg of 50:")
    print(f"   to Luke 4-22 = {r[0]:.3f}   to Acts = {r[1]:.3f}   to Luke 1-3+23-24 = {r[2]:.3f}")
    print(f"   closer to Luke 4-22 than to Acts? {r[0] < r[1]}   closer to 4-22 than Acts is to the padding? {r[0] < dist(acts, pad)}")
