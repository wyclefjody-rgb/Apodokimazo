"""Whole books: do Luke and Acts come out together? And where do the Luke blocks go?
100 MFW (from the whole NT), Eder's Simple, whole-book profiles. Also a Ward tree like Stylo's."""
import sys, os, numpy as np
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load
bk = load("book"); ch = load("chapter")
mfw = [w for w, _ in Counter(w for t in bk.values() for w in t).most_common(100)]
prof = lambda t: np.sqrt(np.array([Counter(t)[w] / len(t) for w in mfw]))
T = dict(bk)
T["Luke 4-22"] = sum((ch[f"Lk {i}"] for i in range(4, 23)), [])
T["Luke 1-3+23-24"] = sum((ch[f"Lk {i}"] for i in (1, 2, 3, 23, 24)), [])
P = {k: prof(v) for k, v in T.items()}
d = lambda a, b: np.abs(P[a] - P[b]).sum()
def show(name, exclude=()):
    others = sorted((d(name, o), o) for o in T if o != name and o not in exclude)[:5]
    print(f"{name:16s} ({len(T[name]):6d} words) -> " + ", ".join(f"{o} ({x:.2f})" for x, o in others))
print("Closest whole books (smaller = more similar):")
for b in ["Lk", "Ac", "Mt", "Mk", "Jn"]: show(b, exclude=("Luke 4-22", "Luke 1-3+23-24"))
print("\nLuke split into blocks (whole Luke left out of the comparison):")
show("Luke 4-22", exclude=("Lk", "Luke 1-3+23-24"))
show("Luke 1-3+23-24", exclude=("Lk", "Luke 4-22"))
# Stylo-style Ward tree on the 26 whole books
try:
    from scipy.cluster.hierarchy import linkage, dendrogram
    names = list(bk); X = np.array([P[n] for n in names])
    D = np.array([[np.abs(a - b).sum() for b in X] for a in X])
    from scipy.spatial.distance import squareform
    Z = linkage(squareform(D, checks=False), "ward")
    order = dendrogram(Z, labels=names, no_plot=True)["ivl"]
    print("\nWard tree leaf order (neighbours in this list sit on nearby branches):\n  " + " | ".join(order))
    # which cluster does Luke first join?
    n = len(names); members = {i: [names[i]] for i in range(n)}
    for i, (a, b, h, _) in enumerate(Z):
        m = members[int(a)] + members[int(b)]; members[n + i] = m
        if "Lk" in m and len(m) > 1:
            print(f"  Luke's first merge: {sorted(m)} at height {h:.2f}"); break
except ImportError:
    print("(scipy not installed: skipped the tree)")
