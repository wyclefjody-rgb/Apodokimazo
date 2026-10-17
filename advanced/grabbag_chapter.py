"""Can you grab-bag a chapter? Tries every way of doing it on all 259 NT chapters and reruns the glom test
(share of chapters whose closest chapter is from the same book), same settings as glom_test.py
(100 MFW from the whole NT, Eder's Simple). Random draws repeat 20 times with a fixed seed.
  A. Chapter as is (the book's way)
  B. Grab bag, same size, no replacement   = Stylo random.sampling with sample.size = chapter length
  C. Grab bag, same size, WITH replacement = Stylo sampling.with.replacement = TRUE
  D. Grab bag, smaller samples (half the chapter, 200 words, 100 words) - Stylo needs sample.size <= length
  E. Grab bag from the WHOLE BOOK, 400 words  = what Eder's random sampling actually does (needs a longer text)
Usage: py -3.12 advanced\\grabbag_chapter.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from load import load
from collections import Counter
rng = np.random.default_rng(7)
ch = load("chapter"); keys = list(ch)
book = lambda k: k.split()[0]
mfw = [w for w, _ in Counter(w for k in keys for w in ch[k]).most_common(100)]
idx = {w: i for i, w in enumerate(mfw)}

def vec(words):
    v = np.zeros(len(mfw)); c = Counter(words)
    for w, n in c.items():
        if w in idx: v[idx[w]] = n / len(words)
    return np.sqrt(v)

def glom(texts):
    V = np.array([vec(texts[k]) for k in keys])
    D = np.abs(V[:, None, :] - V[None, :, :]).sum(2); np.fill_diagonal(D, np.inf)
    nn = D.argmin(1)
    return np.mean([book(keys[i]) == book(keys[j]) for i, j in enumerate(nn)])

def runs(make, n=20):
    r = [glom({k: make(ch[k]) for k in keys}) for _ in range(n)]
    return np.mean(r), np.min(r), np.max(r)

print("Chapter lengths: median", int(np.median([len(ch[k]) for k in keys])), "words")
print(f"\n{'How the sample is made':58s} {'same-book closest':>18s}")
print(f"{'A. Chapter as is (the book)':58s} {glom(ch):>10.0%}")
m = runs(lambda w: list(rng.permutation(w)))
print(f"{'B. Grab bag, same size, no replacement (a shuffle)':58s} {m[0]:>10.0%}   range {m[1]:.0%}-{m[2]:.0%}")
m = runs(lambda w: list(rng.choice(w, len(w), replace=True)))
print(f"{'C. Grab bag, same size, with replacement':58s} {m[0]:>10.0%}   range {m[1]:.0%}-{m[2]:.0%}")
m = runs(lambda w: list(rng.choice(w, max(1, len(w) // 2), replace=False)))
print(f"{'D1. Grab bag, half the chapter':58s} {m[0]:>10.0%}   range {m[1]:.0%}-{m[2]:.0%}")
for n in (200, 100):
    m = runs(lambda w: list(rng.choice(w, min(n, len(w)), replace=False)))
    print(f"{f'D2. Grab bag, {n} words from the chapter':58s} {m[0]:>10.0%}   range {m[1]:.0%}-{m[2]:.0%}")

# E: what random sampling is for - drawing from a longer text. Each chapter is replaced by 400 random words
# from its WHOLE BOOK (books shorter than 400 words are skipped by Stylo; here they keep their own words).
books = {}
for k in keys: books.setdefault(book(k), []).extend(ch[k])
def E():
    t = {k: list(rng.choice(books[book(k)], 400, replace=False)) if len(books[book(k)]) >= 400 else ch[k] for k in keys}
    return glom(t)
r = [E() for _ in range(20)]
print(f"{'E. 400 random words from the whole BOOK (Eder setup)':58s} {np.mean(r):>10.0%}   range {min(r):.0%}-{max(r):.0%}")
print("\nB matches A exactly: shuffling doesn't change word counts. C and D can only lose information,")
print("because every word still comes from the same chapter. E scores high only because it has already")
print("decided which book each sample belongs to - it can't test whether a chapter belongs to its book.")
