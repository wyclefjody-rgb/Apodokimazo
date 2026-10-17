"""Figures 20-23 for the Oct 8-9 Discord findings. Numbers are the outputs of the named scripts (no randomness
except mix_test/direction_test, which use fixed seeds). Run from this folder: py -3.12 today_figures.py"""
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
ACC, GREY, LIGHT, INK, INK2, REF = "#2a78d6", "#a9a7a0", "#d6d4ce", "#0b0b0b", "#52514e", "#8a8882"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": LIGHT, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
def finish(fig, name, title, sub, source):
    fig.text(0.02, 0.97, title, fontsize=14, color=INK, va="top", weight="bold")
    fig.text(0.02, 0.91, sub, fontsize=10.5, color=INK2, va="top")
    fig.text(0.02, 0.015, "Source: " + source, fontsize=8.5, color=INK2)
    fig.subplots_adjust(top=0.78, bottom=0.17)
    fig.savefig(os.path.join(HERE, name), facecolor="white", bbox_inches="tight", pad_inches=0.25); plt.close(fig); print("wrote", name)

# 20: glom test, with and without parallel gospels
labels = ["Mark", "Matthew", "Luke (all 24 ch.)", "John", "Romans", "Core 4 Paul (Ro, 1-2 Co, Ga)"]
allb = [0.38, 0.36, 0.58, 0.95, 0.38, 0.53]; nopar = [0.88, 0.86, 0.92, 1.00, None, None]
fig, ax = plt.subplots(figsize=(9.5, 5.2)); y = np.arange(len(labels))[::-1]; h = 0.36
ax.barh(y + h / 2, allb, height=h, color=GREY, label="All 259 chapters available")
ax.barh([yy - h / 2 for yy, v in zip(y, nopar) if v is not None], [v for v in nopar if v is not None], height=h, color=ACC,
        label="Parallel gospels removed from the comparison")
for yy, v in zip(y, allb): ax.text(v + 0.01, yy + h / 2, f"{v:.0%}", va="center", color=INK, fontsize=10)
for yy, v in zip(y, nopar):
    if v is not None: ax.text(v + 0.01, yy - h / 2, f"{v:.0%}", va="center", color=INK, fontsize=10)
ax.set_yticks(y, labels); ax.set_xlim(0, 1.12); ax.xaxis.set_visible(False); ax.spines["bottom"].set_visible(False); ax.tick_params(axis="y", length=0)
ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.02), ncol=2, frameon=False, fontsize=9.5)
finish(fig, "20_glom_parallels.png", "Single-author gospels 'glom' once shared material is out of the way",
       "Share of chapters whose closest chapter is from the same book (100 MFW, Eder's Simple, SBLGNT)",
       "advanced/glom_test.py, advanced/glom_noparallels.py. Chance is 6-12% for single books, 19% for the core-4 group.")

# 21: blend test
share = [0, 30, 50, 60, 70, 80, 90, 100]
data = {"Hebrews": ([10, 26, 34, 44, 58, 68, 72, 78], [0, 2, 42, 53, 68, 80, 89, 95]),
        "Acts": ([1, 10, 30, 52, 70, 83, 90, 96], [0, 0, 16, 42, 80, 98, 100, 100])}
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
for ax, (other, (s400, s1500)) in zip(axes, data.items()):
    ax.plot(share, s400, color=GREY, lw=2, marker="o", ms=5, label="400 words (chapter length)")
    ax.plot(share, s1500, color=ACC, lw=2, marker="o", ms=5, label="1,500 words")
    ax.axvline(70, color=REF, ls="--", lw=1); ax.text(71, 100, "70% Paul", color=INK2, fontsize=9)
    ax.set_title(f"Romans blended with {other}", fontsize=11, color=INK, loc="left")
    ax.set_xlabel("Share of the blend written by Paul (%)"); ax.set_xticks(share); ax.set_ylim(0, 105); ax.grid(axis="y", color=LIGHT, lw=0.6)
    ax.text(100, s400[-1] - 7, f"{s400[-1]}%", ha="right", color=INK, fontsize=9); ax.text(70, s400[4] + 3, f"{s400[4]}%", ha="right", color=INK, fontsize=9)
    ax.text(70, s1500[4] + 3, f"{s1500[4]}%", ha="left", color=INK, fontsize=9)
axes[0].set_ylabel("Blends siding with Paul (%)"); axes[0].legend(loc="upper left", frameon=False, fontsize=9)
finish(fig, "21_blend_test.png", "A 70% Paul text does not consistently side with Paul",
       "Even pure Romans at 400 words sides with Paul only 78% of the time against Hebrews (400 random blends per point)",
       "advanced/mix_test.py (100 MFW, Eder's Simple; blended passages and reference profiles from different parts of each author)")

# 22: direction test
labs = ["Cut-down Luke  vs  Luke 4-22", "Cut-down Luke  vs  Acts", "Cut-down Luke  vs  Luke 1-3 + 23-24", "Acts  vs  Luke 1-3 + 23-24 (reference)"]
vals = [0.18, 1.40, 1.53, 1.40]
fig, ax = plt.subplots(figsize=(9.5, 3.9)); y = np.arange(len(labs))[::-1]
ax.barh(y, vals, color=[ACC, GREY, GREY, LIGHT], height=0.6)
txt = ["0.14-0.22", "1.40", "1.53", "1.40"]
for yy, v, t in zip(y, vals, txt): ax.text(v + 0.02, yy, t, va="center", color=INK)
ax.set_yticks(y, labs); ax.set_xlim(0, 1.8); ax.xaxis.set_visible(False); ax.spines["bottom"].set_visible(False); ax.tick_params(axis="y", length=0)
finish(fig, "22_direction_test.png", "A Luke cut down Marcion-style shows the 'Evangelion' pattern",
       "Distance (smaller = more similar). Luke 1-3 and 23-24 removed, 15-30% of remaining verses cut at random; held in 50 of 50 random cuts",
       "advanced/direction_test.py (100 MFW, Eder's Simple, SBLGNT)")

# 23: book level, Luke's and Acts' nearest books
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6), sharex=True)
for ax, (book, rows) in zip(axes, {"Luke's closest books": [("Matthew", 0.94), ("Mark", 1.08), ("Acts", 1.27), ("John", 1.75)],
                                   "Acts' closest books": [("Luke", 1.27), ("Matthew", 1.50), ("Hebrews", 1.51), ("Mark", 1.57)]}.items()):
    y = np.arange(len(rows))[::-1]
    ax.barh(y, [v for _, v in rows], color=[ACC if n in ("Acts", "Luke") else GREY for n, _ in rows], height=0.6)
    for yy, (_, v) in zip(y, rows): ax.text(v + 0.02, yy, f"{v:.2f}", va="center", color=INK, fontsize=10)
    ax.set_yticks(y, [n for n, _ in rows]); ax.set_title(book, fontsize=11, color=INK, loc="left")
    ax.set_xlim(0, 2.1); ax.xaxis.set_visible(False); ax.spines["bottom"].set_visible(False); ax.tick_params(axis="y", length=0)
finish(fig, "23_book_level.png", "Whole books: Acts' closest is Luke, but Luke's closest is Matthew",
       "Distance between whole books (smaller = more similar); in a Ward tree Luke joins Matthew first",
       "advanced/book_level.py (100 MFW, Eder's Simple, 26 SBLGNT books)")
