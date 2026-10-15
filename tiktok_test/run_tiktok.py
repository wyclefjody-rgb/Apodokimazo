"""His TikTok test (Jaaron Wingo, CBJ): English, 50 most frequent words, single words, Eder's Delta, cluster tree.
Run on public transcripts: Jaaron (CBJ), Jesus and Whatnot, Born Again Atheist, and the OP's quoted lines."""
import glob, os, re, json, shutil, numpy as np
from collections import Counter
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
rng = np.random.default_rng(3)
tok = lambda s: re.findall(r"[a-z]+(?:'[a-z]+)?", s.lower())
T = {os.path.basename(f)[:-4]: tok(open(f, encoding="utf8").read()) for f in sorted(glob.glob("texts/*.txt"))}
person = lambda k: k.split("_")[0]
pool = {}
for k, v in T.items(): pool.setdefault(person(k), []).append(v)

def eder_delta(texts, n=50, vocab=None):
    top = vocab or [w for w, _ in Counter(t for v in texts for t in v).most_common(n)]
    X = np.array([[Counter(v)[w] / len(v) for w in top] for v in texts])
    Z = (X - X.mean(0)) / (X.std(0) + 1e-12); m = len(top)
    wts = (m - np.arange(1, m + 1) + 1) / m
    return (np.abs(Z[:, None] - Z[None]) * wts).sum(-1) / m, top

def evaluate(labels, texts, vocab=None):
    D, top = eder_delta(texts, vocab=vocab)
    Dz = D.copy(); np.fill_diagonal(Dz, 0)
    root = to_tree(linkage(squareform(Dz, checks=False), "ward")); cl = set()
    def walk(nd):
        cl.add(frozenset(nd.pre_order()))
        if not nd.is_leaf(): walk(nd.left); walk(nd.right)
    walk(root)
    people = {person(l) for l in labels}
    perfect = all(frozenset(i for i, l in enumerate(labels) if person(l) == p) in cl
                  for p in people if sum(person(l) == p for l in labels) > 1)
    np.fill_diagonal(D, np.inf); nn = D.argmin(1)
    multi = [i for i, l in enumerate(labels) if sum(person(m) == person(l) for m in labels) > 1]
    return perfect, float(np.mean([person(labels[nn[i]]) == person(labels[i]) for i in multi])), top

def chunks(words, size):  # non-overlapping pieces, random start
    o = rng.integers(0, max(1, len(words) - size * (len(words) // size) + 1))
    return [words[o + i * size:o + (i + 1) * size] for i in range((len(words) - o) // size)]

R = {}
# A. The files as sent (unequal lengths), his settings
labs = list(T); p, nn, top = evaluate(labs, [T[l] for l in labs])
R["A_files_as_sent"] = {"perfect_tree": p, "closest_same_person": round(nn, 2), "top50": top}

# B. His exact design, equal 130-word files: Jaaron 4, Jesus&Whatnot 2, Born Again Atheist 1, OP 1 -- repeated 300 times
def design_B(vocab_fn=None, size=130):
    J = [c for v in pool["Jaaron"] for c in chunks(v, size)]
    W = [c for v in pool["JesusAndWhatnot"] for c in chunks(v, size)] or []
    Wall = sum(pool["JesusAndWhatnot"], []); Ball = sum(pool["BornAgainAtheist"], [])
    W = chunks(Wall, size); B = chunks(Ball, size); O = pool["OP"][0][:size]
    js = [J[i] for i in rng.choice(len(J), 4, replace=False)]
    ws = [W[i] for i in rng.choice(len(W), 2, replace=False)]
    labels = ["Jaaron_x"] * 4 + ["JesusAndWhatnot_x"] * 2 + ["BornAgainAtheist_x"] + ["OP_x"]
    texts = js + ws + [B[rng.integers(len(B))], O]
    return evaluate(labels, texts, vocab_fn(texts) if vocab_fn else None)

runs = [design_B() for _ in range(300)]
R["B_his_design_130_words_x300"] = {"perfect_tree": round(float(np.mean([r[0] for r in runs])), 3),
                                    "closest_same_person": round(float(np.mean([r[1] for r in runs])), 3)}
# C. Same, but only grammatical words (no topic words like 'stylometry', 'rosary', 'trans')
fw = lambda texts: [w for w, _ in Counter(t for v in texts for t in v).most_common() if w in ENGLISH_STOP_WORDS][:50]
runs = [design_B(fw) for _ in range(300)]
R["C_his_design_function_words_only_x300"] = {"perfect_tree": round(float(np.mean([r[0] for r in runs])), 3),
                                              "closest_same_person": round(float(np.mean([r[1] for r in runs])), 3)}
# D. Does the method split Jaaron himself? All of his text in 130-word pieces, alongside the others' pieces
J = [c for v in pool["Jaaron"] for c in chunks(v, 130)]
others = chunks(sum(pool["JesusAndWhatnot"], []), 130) + chunks(sum(pool["BornAgainAtheist"], []), 130) + [pool["OP"][0]]
labs = [f"Jaaron_{i}" for i in range(len(J))] + [f"JesusAndWhatnot_{i}" for i in range(len(chunks(sum(pool['JesusAndWhatnot'], []), 130)))] \
     + [f"BornAgainAtheist_{i}" for i in range(len(chunks(sum(pool['BornAgainAtheist'], []), 130)))] + ["OP_1"]
p, nn, _ = evaluate(labs, J + others)
R["D_all_Jaaron_pieces"] = {"jaaron_pieces": len(J), "all_on_own_branch": p, "closest_same_person": round(nn, 2)}
topics = [w for w in R["A_files_as_sent"]["top50"] if w not in ENGLISH_STOP_WORDS]
R["topic_words_in_top50"] = topics
json.dump(R, open("tiktok_results.json", "w", encoding="utf8"), indent=1)
for k, v in R.items(): print(k, v if k != "A_files_as_sent" else {x: y for x, y in v.items() if x != "top50"})

# Folders for Stylo trees
for name, files in [("corpus_as_sent", {l: T[l] for l in T})]:
    shutil.rmtree(name, ignore_errors=True); os.makedirs(name)
    for l, t in files.items(): open(f"{name}/{l}.txt", "w", encoding="utf8").write(" ".join(t))
os.makedirs("corpus_his_design", exist_ok=True)
for f in glob.glob("corpus_his_design/*"): os.remove(f)
Jc = [c for v in pool["Jaaron"] for c in chunks(v, 130)]; Wc = chunks(sum(pool["JesusAndWhatnot"], []), 130); Bc = chunks(sum(pool["BornAgainAtheist"], []), 130)
for i, c in enumerate([Jc[0], Jc[1], Jc[-2], Jc[-1]]): open(f"corpus_his_design/Jaaron_{i+1}.txt", "w").write(" ".join(c))
for i, c in enumerate(Wc[:2]): open(f"corpus_his_design/JesusAndWhatnot_{i+1}.txt", "w").write(" ".join(c))
open("corpus_his_design/BornAgainAtheist_1.txt", "w").write(" ".join(Bc[0]))
open("corpus_his_design/OP_1.txt", "w").write(" ".join(pool["OP"][0]))
