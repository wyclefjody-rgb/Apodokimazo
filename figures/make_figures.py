"""Make one PNG per finding, numbered in the order of the argument. Run from this folder:  py -3.12 make_figures.py
Numbers come from the kit's own scripts (named on each figure); the stronger-method figures read advanced/*.json directly.
Trees made by Stylo are copied in from where the other steps saved them, if they exist."""
import json, os, shutil, glob, subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.join(HERE, "..")
ACC, GREY, LIGHT, INK, INK2, REF = "#2a78d6", "#a9a7a0", "#d6d4ce", "#0b0b0b", "#52514e", "#8a8882"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": LIGHT, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})

def finish(fig, ax, name, title, sub, source):
    fig.text(0.02, 0.97, title, fontsize=14, color=INK, va="top", weight="bold")
    fig.text(0.02, 0.91, sub, fontsize=10.5, color=INK2, va="top")
    fig.text(0.02, 0.015, "Source: " + source, fontsize=8.5, color=INK2)
    fig.subplots_adjust(top=0.80, bottom=0.16)
    fig.savefig(os.path.join(HERE, name), facecolor="white", bbox_inches="tight", pad_inches=0.25); plt.close(fig); print("wrote", name)

def hbars(name, title, sub, source, labels, vals, accent_idx=(), ref=None, ref_label="", xmax=1, pct=True):
    fig, ax = plt.subplots(figsize=(9, 0.55 * len(labels) + 2.2))
    y = list(range(len(labels)))[::-1]
    ax.barh(y, vals, color=[ACC if i in accent_idx else GREY for i in range(len(vals))], height=0.6)
    for yi, v in zip(y, vals):
        ax.text(v + xmax * 0.01, yi, f"{v:.0%}" if pct else f"{v:.2f}", va="center", color=INK)
    ax.set_yticks(y, labels); ax.set_xlim(0, xmax); ax.xaxis.set_visible(False); ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    if ref is not None:
        ax.axvline(ref, color=REF, ls="--", lw=1); ax.text(ref, len(labels) - 0.45, ref_label, color=INK2, fontsize=9, ha="left")
    finish(fig, ax, name, title, sub, source)

# 1. signal vs noise
hbars("01_signal_vs_shuffled.png", "About half of chapters sit closest to their own book", "Share of 259 chapters whose nearest neighbour is from the same book, the book's settings (100 MFW, Eder's Simple)",
      "noise_tests/analysis.py", ["Real text", "Real text, function words only", "Shuffled words (average of 20)", "Expected from book sizes alone"],
      [0.52, 0.53, 0.10, 0.06], accent_idx=(0,))
# 2. stability
hbars("02_stability.png", "Most groupings move when the settings change", "How many of the tree's groupings hold up under ordinary changes",
      "consensus_check.R (Stylo consensus, 100-1,000 MFW, 50% rule); noise_tests/analysis.py (45 setting combinations)",
      ["Groupings that pass Stylo's consensus test", "Groupings in all 10 consensus runs", "Pairings that hold in 75% of 45 settings", "Chapters whose nearest neighbour never changes"],
      [0.41, 0.12, 0.22, 0.07], accent_idx=(0, 2))
# 3. novels by length
fig, ax = plt.subplots(figsize=(9, 5))
xs, ys = ["Whole novel", "4,000", "700", "400"], [0.955, 0.597, 0.266, 0.232]
ax.plot(xs, ys, color=ACC, lw=2.5, marker="o", ms=8)
for x, v in zip(xs, ys): ax.text(x, v + 0.04, f"{v:.0%}", ha="center", color=INK)
ax.axhline(0.07, color=REF, ls="--", lw=1); ax.text(3, 0.09, "Chance about 7%", ha="right", color=INK2, fontsize=9)
ax.text(2, 0.18, "a Gospel chapter", ha="center", color=INK2, fontsize=9); ax.text(3, 0.14, "a Pauline chapter", ha="center", color=INK2, fontsize=9)
ax.set_ylim(0, 1.08); ax.set_yticks([0, .25, .5, .75, 1], ["0%", "25%", "50%", "75%", "100%"]); ax.set_xlabel("Sample length (words)")
finish(fig, ax, "03_novels_by_length.png", "Their own English test: 96% on whole novels, 23% at 400 words",
       "22 novels from the book's figure; a piece is correct if its nearest neighbour is a different novel by the same author", "english_demo/english_demo.py")
# 4. speech chapters
hbars("04_speech_chapters.png", "Speeches match speeches: genre, not a new author", "Gospel discourse chapters (19, incl. Mark 13, Matthew 24, Luke 21, John 14-17) whose nearest neighbour is another discourse",
      "book_claims/speech_test.py", ["Discourse chapters", "Expected by chance within the Gospels"], [0.63, 0.20], accent_idx=(0,))
# 5. Septuagint: how much closer to the Septuagint than to the NT (negative = closer to the Septuagint)
lxx = [("Revelation 4-22", 1.99 - 2.12), ("Luke 1-2", 1.95 - 1.79), ("Revelation 2-3", 2.91 - 2.74), ("Revelation 1", 3.19 - 2.95),
       ("Hebrews", 1.67 - 1.40), ("Acts", 1.61 - 1.15), ("Romans", 2.06 - 1.34), ("Mark", 1.69 - 0.99), ("John", 2.20 - 1.37),
       ("Matthew", 1.68 - 0.82), ("Luke 3-24", 1.63 - 0.82)]
fig, ax = plt.subplots(figsize=(9, 6)); y = list(range(len(lxx)))[::-1]
ax.barh(y, [v for _, v in lxx], color=[ACC if n.startswith("Revelation 4") else (INK2 if n == "Luke 1-2" else GREY) for n, _ in lxx], height=0.6)
for yi, (n, v) in zip(y, lxx): ax.text(v + (0.02 if v >= 0 else -0.02), yi, f"{v:+.2f}", va="center", ha="left" if v >= 0 else "right", color=INK)
ax.set_yticks(y, [n for n, _ in lxx]); ax.axvline(0, color=INK2, lw=1); ax.tick_params(axis="y", length=0); ax.set_xlim(-0.3, 0.95)
ax.set_xlabel("Distance to Septuagint minus distance to New Testament  (below 0 = closer to the Septuagint)")
finish(fig, ax, "05_septuagint.png", "Revelation 4-22 leans Septuagint; Luke 1-2, written in Greek, comes next",
       "Eder's Simple, 100 MFW; Revelation 4-22's nearest book is Daniel, Luke 1-2's is Acts", "book_claims/lxx_test.py (Rahlfs Septuagint)")
# 6. blind clustering ARI
fig, ax = plt.subplots(figsize=(9, 5)); g = [3, 5, 8, 12]
ax.plot(g, [0.87, 0.57, 0.35, 0.32], color=GREY, lw=2, marker="o", ms=7); ax.plot(g, [0.37, 0.45, 0.46, 0.47], color=ACC, lw=2.5, marker="o", ms=8)
ax.scatter([8], [0.10], color=REF, s=50, zorder=3); ax.text(8.2, 0.09, "Shuffled words: 0.10", color=INK2, fontsize=9)
ax.text(3.1, 0.89, "Match with genre", color=INK2); ax.text(12, 0.50, "Match with traditional author", color=ACC, ha="right")
ax.set_xticks(g); ax.set_xlabel("Number of blind groups"); ax.set_ylim(0, 1); ax.set_ylabel("Adjusted Rand index (1 = perfect, 0 = chance)")
finish(fig, ax, "06_blind_clustering.png", "Blind, the method sorts by genre first, then by traditional author",
       "All 259 chapters, names hidden and order shuffled, the book's settings", "noise_tests/blind_test.py")
# 7. blind 3 groups composition
fig, ax = plt.subplots(figsize=(9, 3.6)); grp = [("Group 1 (117)", 114, 3, 0), ("Group 2 (24)", 1, 1, 22), ("Group 3 (118)", 5, 113, 0)]
for i, (n, le, na, ap) in enumerate(grp[::-1]):
    ax.barh(i, le, color=ACC, height=0.6); ax.barh(i, na, left=le, color=GREY, height=0.6); ax.barh(i, ap, left=le + na, color=INK2, height=0.6)
ax.set_yticks(range(3), [n for n, *_ in grp[::-1]]); ax.tick_params(axis="y", length=0)
ax.legend(["Letters", "Narrative", "Revelation"], frameon=False, loc="lower right", ncol=3, bbox_to_anchor=(1, -0.45)); ax.set_xlabel("Chapters")
finish(fig, ax, "07_blind_three_groups.png", "Cut into 3 blind groups: letters, Revelation, narrative", "What each blind group turned out to contain",
       "noise_tests/blind_test.py")
# 8-9. stronger methods
cal = json.load(open(os.path.join(KIT, "advanced", "calibration_results.json")))
fig, ax = plt.subplots(figsize=(9, 5)); L = ["250", "400", "700", "1000", "1500", "2500"]
for key, lab, col, lw in [("classifier", "Classifier", GREY, 2), ("cosine", "Cosine, 800 features", LIGHT, 2), ("simple", "Book's method", ACC, 3)]:
    v = [cal["attribution"][s][key] for s in L]; ax.plot(L, v, color=col, lw=lw, marker="o", ms=7, label=lab)
    ax.text(1.08, v[1], f"{v[1]:.0%}", color=INK if col == ACC else INK2, va="center")
ax.axhline(1 / 9, color=REF, ls="--", lw=1); ax.text(0, 0.14, "Chance 11%", ha="left", color=INK2, fontsize=9)
ax.axvline(1, color=REF, ls=":", lw=1); ax.set_ylim(0, 1); ax.set_yticks([0, .25, .5, .75, 1], ["0%", "25%", "50%", "75%", "100%"])
ax.set_xticks(range(6), ["250", "400", "700", "1,000", "1,500", "2,500"]); ax.set_xlabel("Sample length (words)"); ax.legend(frameon=False, loc="lower right")
finish(fig, ax, "08_greek_attribution.png", "At 400 words: 60% with the book's method, 79% with a classifier",
       "Which of 9 Greek authors wrote a sample from a work the method never saw", "advanced/calibrate.py")
fig, ax = plt.subplots(figsize=(9, 5)); L = ["400", "700", "1500", "2500"]
for key, lab, col, lw in [("cosine", "Cosine", GREY, 2), ("gi", "General Impostors", LIGHT, 2), ("simple", "Book's distance", ACC, 3)]:
    ax.plot(L, [cal["verification"][s]["auc"][key] for s in L], color=col, lw=lw, marker="o", ms=7, label=lab)
ax.axhline(0.5, color=REF, ls="--", lw=1); ax.text(3, 0.52, "Coin flip 0.5", ha="right", color=INK2, fontsize=9)
ax.set_ylim(0.4, 1); ax.set_xticks(range(4), ["400", "700", "1,500", "2,500"]); ax.set_xlabel("Sample length (words)"); ax.set_ylabel("AUC (1 = always right)")
ax.legend(frameon=False, loc="lower right")
finish(fig, ax, "09_greek_verification.png", "Are two short samples by the same author? Hard to tell below 2,500 words",
       "Pairs of samples from different works by 9 Greek authors; AUC = how often a same-author pair outranks a different-author pair", "advanced/calibrate.py")
nt = json.load(open(os.path.join(KIT, "advanced", "nt_results.json")))
rows = [("Romans, 1-2 Cor., Galatians together", "Paul core letters with each other"), ("Core with Philippians, 1 Thess.", "Paul core with Philippians / 1 Thessalonians"),
        ("Acts 1-12 with 13-28 (one author)", "Acts 1-12 with Acts 13-28 (one author)"), ("John with 1 John", "Gospel of John with 1 John (often one author)"),
        ("Core Paul vs 1 Peter", "Paul core with 1Pe"), ("Core Paul vs James", "Paul core with Jas"), ("Core Paul vs Colossians", "Paul core with Col"),
        ("Luke with Acts", "Luke with Acts (traditionally one author)"), ("Core Paul vs Ephesians", "Paul core with Eph"), ("Core Paul vs Ignatius", "Paul core with Ignatius"),
        ("Core Paul vs Pastorals", "Paul core with Pastorals"), ("Core Paul vs Hebrews", "Paul core with Heb"), ("Core Paul vs John", "Paul core with Jn"),
        ("Core Paul vs Barnabas", "Paul core with Barnabas"), ("Core Paul vs 1 Clement", "Paul core with 1Clement"), ("Core Paul vs Acts", "Paul core with Ac"),
        ("Core Paul vs Revelation", "Paul core with Re")]
fig, ax = plt.subplots(figsize=(9, 8)); y = list(range(len(rows)))[::-1]
for yi, (lab, key) in zip(y, rows):
    a, b = nt["400"][key]["median_gi"], nt["1500"][key]["median_gi"]; col = ACC if "core letters" in key.lower() or "philippians" in key.lower() else (INK2 if "(" in key else GREY)
    ax.plot([a, b], [yi, yi], color=col, lw=1.5, alpha=0.6); ax.scatter([a], [yi], facecolors="white", edgecolors=col, s=40, zorder=3); ax.scatter([b], [yi], color=col, s=55, zorder=3)
    if b >= 0.3: ax.text(max(a, b) + 0.02, yi, f"{b:.2f}", va="center", color=INK)
ax.set_yticks(y, [r[0] for r in rows]); ax.tick_params(axis="y", length=0); ax.set_xlim(0, 1.08)
ax.axvline(nt["1500"]["Known Greek authors: same author, different works"]["median_gi"], color=REF, ls="--", lw=1)
ax.scatter([], [], facecolors="white", edgecolors=GREY, label="400 words"); ax.scatter([], [], color=GREY, label="1,500 words"); ax.legend(frameon=False, loc="lower right")
ax.set_xlabel("General Impostors score (0 = never closer than other writers, 1 = always)")
finish(fig, ax, "10_paul_verification.png", "Paul's core letters match each other (0.96) as closely as Acts matches itself",
       "Median of 30 draws per comparison. Dashed line: typical same-author score for known Greek writers (0.40)", "advanced/nt_apply.py")

# trees made by Stylo, copied in with the same numbering. The newest run on this computer wins; the kit's bundled images are the fallback.
def newest(*patterns):
    hits = [f for p in patterns for f in glob.glob(os.path.join(KIT, p))]
    return max(hits, key=os.path.getmtime) if hits else None
def pdf2png(pdf, out):
    if shutil.which("pdftoppm"):
        subprocess.run(["pdftoppm", "-png", "-r", "110", "-singlefile", pdf, os.path.join(HERE, out[:-4])]); print("wrote", out)
    else:
        shutil.copy(pdf, os.path.join(HERE, out[:-4] + ".pdf")); print("copied", out[:-4] + ".pdf (no PNG found; rerun Rscript run_stylo.R)")
TREES = [("11_tree_novels_whole.png", ["english_demo/tree_whole/*.png", "english_demo/tree_whole_novels.png"]),
         ("12_tree_novels_400_words.png", ["english_demo/tree_400/*.png", "english_demo/tree_400_words.png"]),
         ("13_tree_acts_alone.png", ["output/3_acts/*.png", "output/3_acts/*__001.pdf"]),
         ("14_tree_whole_books.png", ["output/4_books/*.png", "output/4_books/*__001.pdf"]),
         ("15_tree_greek_demo.png", ["greek_demo/tree_their_demo/*.png", "greek_demo/greek_demo_tree.png"]),
         ("16_tree_exhibit6_with_justin.png", ["greek_demo/tree_exhibit6_control/*.png", "greek_demo/exhibit6_control_tree.png"]),
         ("17_tree_tiktok_test.png", ["tiktok_test/tree_his_design/*.png", "tiktok_test/tiktok_tree_his_design.png"]),
         ("18_tree_consensus_all_chapters.png", ["output/2_consensus/*.png", "output/2_consensus/*__001.pdf"]),
         ("19_tree_all_259_chapters.png", ["output/1_all_chapters/*.png", "output/1_all_chapters/*__001.pdf"])]
for out, pats in TREES:
    png = newest(*[p for p in pats if p.endswith(".png")]); pdf = newest(*[p for p in pats if p.endswith(".pdf")])
    if png: shutil.copy(png, os.path.join(HERE, out)); print("copied", out)
    elif pdf: pdf2png(pdf, out)
    else: print("missing", out, "- run the step that makes it first")
