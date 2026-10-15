"""Shared pieces: texts, chunks, features, distances, General Impostors."""
import json, os, sys, numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "noise_tests"))
from load import load as nt_load

G = json.load(open(os.path.join(HERE, "greek_reference.json"), encoding="utf8"))
AUTH = G["authors"]                         # author -> work -> tokens
nt_ch = nt_load("chapter")
def nt(book, a=None, b=None):
    return sum([v for k, v in nt_ch.items() if k.split(" ")[0] == book and
                (a is None or (k.count(" ") and a <= int(k.split(" ")[1]) <= b))], [])
NT = {b: nt(b) for b in ["Mt","Mk","Lk","Jn","Ac","Ro","1Co","2Co","Ga","Eph","Php","Col","1Th","2Th","Heb","Jas","1Pe","1Jn","Re"]}
NT["Pastorals"] = nt("1Ti") + nt("2Ti") + nt("Tit")
NT["Acts1-12"] = nt("Ac", 1, 12); NT["Acts13-28"] = nt("Ac", 13, 28)
OTHER = {k: v for k, v in G["other"].items() if len(v) > 3000}   # 1 Clement, Ignatius, Barnabas, Tatian

def chunk(tokens, n, rng):
    if len(tokens) <= n: return tokens
    s = rng.integers(0, len(tokens) - n); return tokens[s:s + n]

# fixed feature list, chosen once from everything pooled (standard practice; no labels involved)
_pool_w = Counter(); _pool_c = Counter()
for src in list(AUTH.values()):
    for t in src.values(): _pool_w.update(t)
for t in list(NT.values()) + list(OTHER.values()): _pool_w.update(t)
WORDS = [w for w, _ in _pool_w.most_common(300)]
def trigrams(tokens):
    s = " " + " ".join(tokens) + " "; return [s[i:i+3] for i in range(len(s) - 2)]
for src in list(AUTH.values()):
    for t in src.values(): _pool_c.update(trigrams(t[:20000]))
for t in list(NT.values()) + list(OTHER.values()): _pool_c.update(trigrams(t))
CHARS = [c for c, _ in _pool_c.most_common(500)]
WI = {w: i for i, w in enumerate(WORDS)}; CI = {c: i for i, c in enumerate(CHARS)}

def feats(tokens):
    """Relative frequencies: 300 words + 500 letter-trigrams."""
    v = np.zeros(800)
    for w, c in Counter(tokens).items():
        if w in WI: v[WI[w]] = c / len(tokens)
    tg = trigrams(tokens)
    for g, c in Counter(tg).items():
        if g in CI: v[300 + CI[g]] = c / len(tg)
    return v

def simple(a, b):
    """Stylo's Eder's Simple on the 100 most frequent words: Manhattan distance of square-rooted frequencies."""
    return np.abs(np.sqrt(a[:100]) - np.sqrt(b[:100])).sum()

class Scaler:
    def __init__(self, X): self.m = X.mean(0); self.s = X.std(0) + 1e-9
    def __call__(self, X): return (X - self.m) / self.s

def cos_sim(A, B):
    A = A / np.linalg.norm(A, axis=-1, keepdims=True); B = B / np.linalg.norm(B, axis=-1, keepdims=True)
    return A @ B.T

def impostors(x, y, imp, rng, k=100, frac=0.5):
    """General Impostors (Koppel & Winter 2014): share of random feature subsets where y is closer to x than every impostor,
    averaged both ways. x, y: z-scored vectors; imp: matrix of z-scored impostor chunks."""
    hits = 0
    for _ in range(k):
        f = rng.random(x.shape[0]) < frac
        for a, b in ((x, y), (y, x)):
            s_ab = cos_sim(a[f][None], b[f][None])[0, 0]
            s_ai = cos_sim(a[f][None], imp[:, f]).max()
            hits += s_ab > s_ai
    return hits / (2 * k)
