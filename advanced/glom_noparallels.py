"""Glom test with the parallel gospels removed from the comparison pool.
If Mark's low score was caused by its Matthew/Luke parallels, Mark should cluster much better
once those books can't be picked. Same settings: 100 MFW (whole NT), Eder's Simple."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load
from collections import Counter
ch = load("chapter"); keys = list(ch)
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
V = {k: np.sqrt(np.array([Counter(ch[k])[w] / len(ch[k]) for w in mfw])) for k in keys}
b = lambda k: k.split()[0]; c = lambda k: int(k.split()[1]) if " " in k else 0
def run(name, inside, exclude):
    pool = [k for k in keys if b(k) not in exclude]
    mine = [k for k in pool if inside(k)]; hit = 0; misses = []
    for k in mine:
        nn = min((np.abs(V[k] - V[j]).sum(), j) for j in pool if j != k)[1]
        if inside(nn): hit += 1
        else: misses.append(f"{k}->{nn}")
    chance = (len(mine) - 1) / (len(pool) - 1)
    print(f"{name:45s} {hit:2d}/{len(mine):2d} ({hit/len(mine):4.0%})  chance {chance:4.0%}")
    if misses: print("     misses:", ", ".join(misses))
run("Mark, all books available", lambda k: b(k) == "Mk", [])
run("Mark, Matthew & Luke removed", lambda k: b(k) == "Mk", ["Mt", "Lk"])
run("Mark 1-15 (no longer ending), Mt & Lk removed", lambda k: b(k) == "Mk" and c(k) <= 15, ["Mt", "Lk"])
run("Luke 4-22, all books available", lambda k: b(k) == "Lk" and 4 <= c(k) <= 22, [])
run("Luke 4-22, Matthew & Mark removed", lambda k: b(k) == "Lk" and 4 <= c(k) <= 22, ["Mt", "Mk"])
run("Romans, all books available", lambda k: b(k) == "Ro", [])
run("Core 4 Paul, all books available", lambda k: b(k) in ("Ro", "1Co", "2Co", "Ga"), [])
print("\nOther gospels the same way:")
run("Matthew, Mark & Luke removed", lambda k: b(k) == "Mt", ["Mk", "Lk"])
run("Luke (all 24), Matthew & Mark removed", lambda k: b(k) == "Lk", ["Mt", "Mk"])
run("Luke (all 24), Mt, Mk AND Acts removed", lambda k: b(k) == "Lk", ["Mt", "Mk", "Ac"])
run("John, Mt, Mk & Lk removed", lambda k: b(k) == "Jn", ["Mt", "Mk", "Lk"])
# where do the core-letter chapters' closest matches land?
core = ("Ro", "1Co", "2Co", "Ga"); und = core + ("Php", "1Th", "Phm"); allp = und + ("Eph", "Col", "2Th", "1Ti", "2Ti", "Tit")
mine = [k for k in keys if b(k) in core]
nnc = {k: min((np.abs(V[k] - V[j]).sum(), j) for j in keys if j != k)[1] for k in mine}
print(f"\nCore 4 Paul chapters ({len(mine)}): closest match in a core letter {sum(b(v) in core for v in nnc.values())}, "
      f"in any undisputed letter {sum(b(v) in und for v in nnc.values())}, in any letter carrying Paul's name {sum(b(v) in allp for v in nnc.values())}")
print("   others:", dict(Counter(b(v) for v in nnc.values() if b(v) not in allp)))
