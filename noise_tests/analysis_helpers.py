import os
import numpy as np
from collections import Counter
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist
def freq_matrix(texts, n_mfw, vocab=None):
    labels = list(texts)
    if vocab is None:
        tot = Counter(t for toks in texts.values() for t in toks)
        vocab = [w for w, _ in tot.most_common(n_mfw)]
    idx = {w: i for i, w in enumerate(vocab)}
    X = np.zeros((len(labels), len(vocab)))
    for r, l in enumerate(labels):
        c = Counter(texts[l])
        n = len(texts[l])
        for w, k in c.items():
            if w in idx:
                X[r, idx[w]] = k / n
    return labels, X, vocab


def delta(X, kind="classic"):
    Z = (X - X.mean(0)) / (X.std(0) + 1e-12)
    if kind == "classic":
        return pdist(Z, "cityblock") / X.shape[1]
    if kind == "cosine":
        return pdist(Z, "cosine")
    if kind == "simple":  # Eder's Simple: Manhattan on square-rooted relative frequencies
        return pdist(np.sqrt(X), "cityblock")
    if kind == "eder":
        return pdist(Z, "euclidean")


import os
DIST=os.environ.get("DIST","simple")
def cluster(texts, n_mfw=100, dist=DIST, link="ward", vocab=None):
    labels, X, vocab = freq_matrix(texts, n_mfw, vocab)
    D = delta(X, dist)
    L = linkage(D, method=link)
    return labels, D, L


