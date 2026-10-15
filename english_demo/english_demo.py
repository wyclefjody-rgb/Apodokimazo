"""Re-run the book's English demo (Chapter 7) the way they ran it, then cut the same novels to New Testament chapter sizes.

The book's figure shows these 22 novels from Stylo's "100 English novels" collection, plus one Harry Potter book.
Harry Potter is still under copyright, so it isn't included. If you own a copy, save it as plain text named
    Rowling_HarryPotter2_1998.txt
in this folder and it will be added automatically.

Settings are the ones printed on their figure: 100 most frequent words, culling 0%, Eder's Simple distance.
Usage:  python3 english_demo.py path/to/100_english_novels/corpus
"""
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import glob, json, os, re, shutil, sys
import numpy as np
from collections import Counter

SRC = sys.argv[1] if len(sys.argv) > 1 else "100_english_novels/corpus"
THEIRS = ["Blackmore_Springhaven_1887", "Blackmore_Erema_1877", "Blackmore_Lorna_1869",
          "Dickens_Expectations_1861", "Dickens_Bleak_1853", "Eliot_Daniel_1876", "Eliot_Adam_1859",
          "Cbronte_Shirley_1849", "Cbronte_Jane_1847", "Cbronte_Villette_1853",
          "Thackeray_Pendennis_1850", "Thackeray_Esmond_1852", "Thackeray_Virginians_1859",
          "Stevenson_Treasure_1883", "Stevenson_Arrow_1888", "Doyle_Lost_1912", "Doyle_Hound_1902",
          "Chesterton_Thursday_1908", "Chesterton_Napoleon_1904", "Chesterton_Innocence_1911",
          "Woolf_Years_1937", "Woolf_Lighthouse_1927"]
HERE = os.path.dirname(os.path.abspath(__file__))
tok = lambda s: re.findall(r"[a-z]+(?:'[a-z]+)?", s.lower())
novels = {n: tok(open(f"{SRC}/{n}.txt", encoding="utf8", errors="ignore").read()) for n in THEIRS}
hp = os.path.join(HERE, "Rowling_HarryPotter2_1998.txt")
if os.path.exists(hp):
    novels["Rowling_HarryPotter2_1998"] = tok(open(hp, encoding="utf8", errors="ignore").read())
author = lambda k: k.split("_")[0]
rng = np.random.default_rng(1)


def dist(texts):
    top = [w for w, _ in Counter(t for v in texts for t in v).most_common(100)]
    S = np.sqrt(np.array([[Counter(v)[w] / len(v) for w in top] for v in texts]))
    D = np.abs(S[:, None] - S[None]).sum(-1)
    np.fill_diagonal(D, np.inf)
    return D


def pieces(size, per_novel=4):
    labs, txt = [], []
    for k, t in novels.items():
        starts = sorted(rng.choice(len(t) - size, per_novel, replace=False)) if size else [None]
        for i, o in enumerate(starts):
            labs.append(f"{k}_{i+1}" if size else k)
            txt.append(t if size is None else t[o:o + size])
    return labs, txt


def score(labs, txt):
    D = dist(txt)
    novel = lambda l: "_".join(l.split("_")[:3])
    multi = {a for a in map(author, novels) if sum(author(n) == a for n in novels) > 1}
    ok = []
    for i, l in enumerate(labs):
        if author(l) not in multi:
            continue                                   # an author with one book has nothing to match
        d = D[i].copy()
        for j, m in enumerate(labs):
            if novel(m) == novel(l):
                d[j] = np.inf                          # must match a DIFFERENT book by the same author
        ok.append(author(labs[d.argmin()]) == author(l))
    return float(np.mean(ok))


def write_corpus(folder, labs, txt):
    shutil.rmtree(folder, ignore_errors=True); os.makedirs(folder)
    for l, t in zip(labs, txt):
        open(f"{folder}/{l}.txt", "w", encoding="utf8").write(" ".join(t))


results = {}
for name, size in [("whole novels", None), ("4,000 words (a novel chapter)", 4000),
                   ("700 words (their Gospel chapter)", 700), ("400 words (their Pauline chapter)", 400)]:
    accs = []
    for rep in range(1 if size is None else 20):
        labs, txt = pieces(size)
        accs.append(score(labs, txt))
        if rep == 0:
            write_corpus(os.path.join(HERE, "corpus_" + ("whole" if size is None else str(size))), labs, txt)
    results[name] = round(float(np.mean(accs)), 3)
    print(f"{name:36s} correct author (a different book by the same writer): {np.mean(accs):.0%}")
json.dump(results, open(os.path.join(HERE, "english_demo_results.json"), "w", encoding="utf8"), indent=1)
