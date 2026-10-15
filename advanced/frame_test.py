"""Do letter openings/closings group together regardless of letter? (Romans 1, 15, 16 question)
Stylo-style: 100 MFW from Paul's undisputed chapters, Eder's Simple distance."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load
from collections import Counter
ch = load("chapter")
PAUL = ["Ro", "1Co", "2Co", "Ga", "Php", "1Th"]
keys = [k for k in ch if k.split()[0] in PAUL]
last = {b: max(int(k.split()[1]) for k in keys if k.split()[0] == b) for b in PAUL}
FRAME = {f"{b} 1" for b in PAUL} | {f"{b} {last[b]}" for b in PAUL} | {"Ro 15"}
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
def vec(t):
    c = Counter(t); return np.array([c[w] / len(t) for w in mfw])
V = {k: vec(ch[k]) for k in keys}
d = lambda a, b: np.abs(np.sqrt(V[a]) - np.sqrt(V[b])).sum()
print("words:", {k: len(ch[k]) for k in ["Ro 1", "Ro 15", "Ro 16"]})
print("Jesus (Ἰησοῦς, all forms) in Romans:", sum(1 for k in keys if k.startswith("Ro ") for w in ch[k] if w.startswith("ιησου")))
print("God (θεος forms) in Romans:", sum(1 for k in keys if k.startswith("Ro ") for w in ch[k] if w.startswith("θε") and w[:4] in ("θεοσ","θεου","θεω","θεον")))
print("\nNearest 3 chapters (Simple, 100 MFW) for Romans 1, 15, 16:")
for k in ["Ro 1", "Ro 15", "Ro 16"]:
    nn = sorted((d(k, j), j) for j in keys if j != k)[:3]
    print(f"  {k:6s} ->", ", ".join(f"{j}{'*' if j in FRAME else ''}" for _, j in nn))
# are frame chapters closer to OTHER letters' frames than to own letter's middle chapters?
fr = [k for k in keys if k in FRAME]; mid = [k for k in keys if k not in FRAME]
within = np.mean([d(a, b) for a in fr for b in fr if a < b and a.split()[0] != b.split()[0]])
to_own_mid = np.mean([d(a, b) for a in fr for b in mid if a.split()[0] == b.split()[0]])
mid_mid = np.mean([d(a, b) for a in mid for b in mid if a < b and a.split()[0] == b.split()[0]])
print(f"\nAvg distance: frame chapter vs other letters' frames = {within:.3f}")
print(f"Avg distance: frame chapter vs its OWN letter's middle chapters = {to_own_mid:.3f}")
print(f"Avg distance: middle vs middle chapters of same letter = {mid_mid:.3f}")
# nearest-neighbour: how often is a frame chapter's nearest neighbour another frame chapter?
hits = sum(min(((d(a, j), j) for j in keys if j != a))[1] in FRAME for a in fr)
print(f"Frame chapters whose nearest neighbour is another frame chapter: {hits}/{len(fr)} (frames are {len(fr)-1}/{len(keys)-1} = {(len(fr)-1)/(len(keys)-1):.0%} of candidates)")
