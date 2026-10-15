"""Run every test in this kit, in order, on Windows, Mac or Linux.

    python run_all.py          (Windows)
    python3 run_all.py         (Mac / Linux)

Needs Python 3 with numpy, scipy and scikit-learn, and R with the stylo and ape packages (see README).
The two extra text collections (English novels, Greek Septuagint) are downloaded automatically with git
the first time; if git isn't installed, the README says how to download them by hand.
Takes about 5 minutes. Everything prints here, and the trees are saved in the output folders.
"""
import os, shutil, subprocess, sys

for _s in (sys.stdout, sys.stderr):      # Greek output must not crash an older Windows console
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
def find_rscript():
    """Find Rscript even when R isn't on the PATH (the normal case on Windows)."""
    hit = shutil.which("Rscript") or shutil.which("Rscript.exe")
    if hit:
        return hit
    import glob
    pats = [r"C:\Program Files\R\R-*\bin\Rscript.exe",
            r"C:\Program Files (x86)\R\R-*\bin\Rscript.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\R\R-*\bin\Rscript.exe"),
            "/Library/Frameworks/R.framework/Resources/bin/Rscript",
            "/opt/homebrew/bin/Rscript", "/usr/local/bin/Rscript"]
    found = sorted(f for p in pats for f in glob.glob(p))
    return found[-1] if found else None   # newest version if several are installed


RSCRIPT = find_rscript()
print("Using R at:", RSCRIPT or "not found (Stylo steps will be skipped; see README)")


def step(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70, flush=True)


def run(cmd, cwd=HERE, env=None, quiet_filter=None):
    e = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", **(env or {}))   # Greek text needs UTF-8 on Windows
    p = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, stdin=subprocess.DEVNULL, text=True, encoding="utf8", errors="replace")
    out = p.stdout + ("" if p.returncode == 0 else p.stderr)
    for line in out.splitlines():
        if quiet_filter is None or quiet_filter(line) or p.returncode != 0:
            print(line)
    if p.returncode != 0:
        print(f"  (this step failed; see the message above)")
    return p.returncode == 0


def fetch(folder, url):
    path = os.path.join(HERE, folder)
    if os.path.isdir(path):
        return True
    if not shutil.which("git"):
        print(f"  git isn't installed. Download {url} as a ZIP, unzip it here, and name the folder '{folder}'.")
        return False
    print(f"  downloading {url} ...")
    return run(["git", "clone", "-q", "--depth", "1", url, folder])


step("1. Building the Greek chapter files")
run([PY, "make_corpus.py", "sblgnt"])

step("2. Stylo with the book's settings (100 words, Eder's Simple): trees, consensus check, Acts control")
print("  (This step takes 1-3 minutes and prints nothing until it finishes.)", flush=True)
if RSCRIPT:
    keep = lambda l: any(k in l for k in ("Nearest neighbour", "Ac_", "$", "Groupings", "Chapters left", "Done"))
    run([RSCRIPT, "run_stylo.R"], quiet_filter=keep)
    run([RSCRIPT, "consensus_check.R"], quiet_filter=keep)
else:
    print("  R isn't installed, so the Stylo steps are skipped. The Python steps below still run.")

step("3. Paul: one voice or a group?")
run([PY, "paul_test.py"])

step("4. Noise tests: sample size, 45 setting combinations, shuffled text")
print("  (About 1 minute.)", flush=True)
os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
nt = os.path.join(HERE, "noise_tests")
run([PY, "analysis.py"], cwd=nt, quiet_filter=lambda l: False)
run([PY, "chunk.py"], cwd=nt, quiet_filter=lambda l: False)
run([PY, "-c", (
    "import json\n"
    "R=json.load(open('results_simple.json',encoding='utf8')); C=json.load(open('chunk_simple.json'))\n"
    "print(f\"Closest chapter is from the same book: {R['base_nn_same_book']:.0%} (shuffled words: {R['null_nn_same_book_mean']:.0%})\")\n"
    "print(f\"Tree pairings that hold in 75% of 45 setting combinations: {R['default_pairs_that_survive_75pct']:.0%}\")\n"
    "print(f\"Chapters whose closest match changes with the settings: {R['nn_changes_share']:.0%}\")\n"
    "print('Identifying which of 10 books a sample came from:')\n"
    "[print(f\"  {p['size']:>5} words: {p['acc']:.0%} correct\") for p in C['curve']]\n")], cwd=nt)

step("4b. Blind test: every chapter with no names, grouped by style alone")
run([PY, "blind_test.py"], cwd=nt)
print("\n--- Stronger features (words + letter sequences + grammar tags) ---")
run([PY, "blind_rich.py"], cwd=nt)
print("\n--- Stronger features, 1,500-word blocks ---")
run([PY, "blind_blocks.py"], cwd=nt, quiet_filter=lambda l: "blocks of" in l or l.startswith(("8 ","12 ","  ","Closest","Core","Same","   (")))

step("5. The book's own claims: novels at chapter length, Matthew vs Mark, 'theological words'")
bc = os.path.join(HERE, "book_claims")
run([PY, "their_claims.py"], cwd=bc)

step("6. Speech chapters (Mark 13, John 14-17)")
run([PY, "speech_test.py"], cwd=bc)

step("7. Revelation 4-22 and Luke 1-2 against the Greek Septuagint")
if fetch("lxx", "https://github.com/eliranwong/LXX-Rahlfs-1935"):
    run([PY, "lxx_test.py"], cwd=bc, env={"LXX": os.path.join(HERE, "lxx")})

step("8. The book's English demo, rerun, then cut to chapter sizes")
print("  (1-2 minutes, plus a download the first time.)", flush=True)
if fetch("100_english_novels", "https://github.com/computationalstylistics/100_english_novels"):
    ed = os.path.join(HERE, "english_demo")
    run([PY, "english_demo.py", os.path.join(HERE, "100_english_novels", "corpus")], cwd=ed)
    if RSCRIPT:
        run([RSCRIPT, "trees.R"], cwd=ed, quiet_filter=lambda l: False)
        print("  Trees saved in english_demo/tree_whole and english_demo/tree_400")

step("9. Stronger methods: error rates on known Greek authors, authorship verification, likelihood ratios")
adv = os.path.join(HERE, "advanced")
GENV = {"PERSEUS": os.path.join(HERE, "canonical-greekLit"), "FIRST1K": os.path.join(HERE, "First1KGreek")}
if os.path.exists(os.path.join(adv, "greek_reference.json")) or run([PY, "build_greek.py"], cwd=adv, env=GENV):
    print("  (About 8 minutes.)", flush=True)
    run([PY, "calibrate.py"], cwd=adv, quiet_filter=lambda l: "Warning" not in l and "iter" not in l)
    run([PY, "nt_apply.py"], cwd=adv)
else:
    print("  Needs the Greek collections; see advanced/README.md")

step("10. The TikTok test and the Greek demo trees")
tk = os.path.join(HERE, "tiktok_test")
run([PY, "run_tiktok.py"], cwd=tk)
if RSCRIPT: run([RSCRIPT, "trees.R"], cwd=tk, quiet_filter=lambda l: False)
gd = os.path.join(HERE, "greek_demo")
if os.path.isdir(os.path.join(HERE, "canonical-greekLit")) and os.path.isdir(os.path.join(HERE, "First1KGreek")):
    run([PY, "build.py"], cwd=gd, quiet_filter=lambda l: False)
    run([PY, "analyze.py"], cwd=gd)
    if RSCRIPT: run([RSCRIPT, "trees.R"], cwd=gd, quiet_filter=lambda l: False)
else:
    print("  The Greek demo needs two downloads (see greek_demo/README.md); the bundled tree images will be used instead.")

step("11. Every figure as a PNG, in the figures folder")
try:
    import matplotlib  # noqa
    run([PY, "make_figures.py"], cwd=os.path.join(HERE, "figures"))
    print("  Open the figures folder: 01-10 are charts, 11-19 are trees. figures/README.md says what each shows.")
except ImportError:
    print("  Needs matplotlib:  py -3.12 -m pip install matplotlib   then run this again.")

print("\nDone. Trees (PDF/PNG) are in the output folder and english_demo/.")
