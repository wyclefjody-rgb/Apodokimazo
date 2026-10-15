"""'Do the chapters glom together?' Nearest-neighbour test on all 259 NT chapters, Stylo-style
(100 MFW from the whole NT, Eder's Simple). For each group: share of its chapters whose closest
chapter is in the same group, vs what chance would give."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load
from collections import Counter
ch = load("chapter"); keys = list(ch)
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
V = {k: np.sqrt(np.array([Counter(ch[k])[w] / len(ch[k]) for w in mfw])) for k in keys}
nn = {k: min((np.abs(V[k] - V[j]).sum(), j) for j in keys if j != k)[1] for k in keys}
b = lambda k: k.split()[0]; c = lambda k: int(k.split()[1]) if " " in k else 0
GROUPS = {
 "Luke 4-22 (canonical)": lambda k: b(k) == "Lk" and 4 <= c(k) <= 22,
 "Mark (one author)": lambda k: b(k) == "Mk",
 "Acts (one author)": lambda k: b(k) == "Ac",
 "Romans": lambda k: b(k) == "Ro",
 "1 Corinthians": lambda k: b(k) == "1Co",
 "2 Corinthians": lambda k: b(k) == "2Co",
 "Galatians": lambda k: b(k) == "Ga",
 "Core 4 Paul (Ro,1-2Co,Ga)": lambda k: b(k) in ("Ro", "1Co", "2Co", "Ga"),
 "Revelation (one author)": lambda k: b(k) == "Re",
}
print(f"{'group':28s} {'chapters':>8s} {'NN in group':>12s} {'chance':>7s}")
for g, f in GROUPS.items():
    m = [k for k in keys if f(k)]; hit = sum(f(nn[k]) for k in m)
    print(f"{g:28s} {len(m):8d} {hit:6d} ({hit/len(m):4.0%}) {(len(m)-1)/(len(keys)-1):7.0%}")
print("\nLuke 4-22 chapters whose nearest neighbour is NOT in Luke 4-22:")
print("  ", ", ".join(f"{k}->{nn[k]}" for k in keys if GROUPS['Luke 4-22 (canonical)'](k) and not GROUPS['Luke 4-22 (canonical)'](nn[k])))
