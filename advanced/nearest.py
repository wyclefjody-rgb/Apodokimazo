"""Closest chapters for every chapter of one book, Stylo-style (100 MFW from the whole NT, Eder's Simple).
Usage:  py -3.12 advanced\nearest.py 1Th        (book codes: Mt Mk Lk Jn Ac Ro 1Co 2Co Ga Eph Php Col 1Th 2Th 1Ti 2Ti Tit Phm Heb Jas 1Pe 2Pe 1Jn Jud Re)
Optional 2nd number = how many neighbours to show (default 3)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load
from collections import Counter
book = sys.argv[1] if len(sys.argv) > 1 else "1Th"; n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
ch = load("chapter"); keys = list(ch)
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
V = {k: np.sqrt(np.array([Counter(ch[k])[w] / len(ch[k]) for w in mfw])) for k in keys}
mine = [k for k in keys if k.split()[0] == book]
if not mine: sys.exit(f"No chapters found for '{book}'. Use a code like 1Th, Ro, 1Co, Lk, Mk.")
print(f"{'chapter':9s} {'words':>5s}   closest {n} (distance)")
for k in mine:
    top = sorted((np.abs(V[k] - V[j]).sum(), j) for j in keys if j != k)[:n]
    print(f"{k:9s} {len(ch[k]):5d}   " + ", ".join(f"{j} ({d:.2f})" for d, j in top))
