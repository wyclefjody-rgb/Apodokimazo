"""Recreate the kit's environment on a new computer from the code alone.
Checks each input the scripts need and downloads or builds only what is missing.

Usage (from the kit folder):   py -3.12 setup_data.py
Needs: Python 3, git (git-scm.com), an internet connection. Safe to run again: anything present is left alone.

What it fetches (all free, openly licensed; credit them if you redistribute):
  sblgnt/              MorphGNT SBLGNT (SBLGNT EULA + CC BY-SA 3.0)   github.com/morphgnt/sblgnt
  100_english_novels/  Stylo's benchmark novels (public domain)      github.com/computationalstylistics/100_english_novels
  g1.xml, g2.xml       Ignatius, genuine + long recension (CC BY-SA)  First1KGreek tlg1443
  canonical-greekLit/  Perseus Greek texts, only the authors needed     github.com/PerseusDL/canonical-greekLit
  First1KGreek/        Open Greek and Latin, only the authors needed   github.com/OpenGreekAndLatin/First1KGreek
Then it builds: corpus_nt_chapters/ (make_corpus.py), advanced/greek_reference.json (advanced/build_greek.py)
and advanced/letters_reference.json (advanced/build_letters.py).
"""
import os, sys, subprocess, urllib.request, shutil, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
J = lambda *p: os.path.join(HERE, *p)

def run(cmd, cwd=HERE):
    print("   $", " ".join(cmd)); subprocess.run(cmd, cwd=cwd, check=True)

def need(label, path):
    ok = os.path.exists(path) and (not os.path.isdir(path) or os.listdir(path))
    print(("OK      " if ok else "MISSING ") + label)
    return not ok

def git_ok():
    if shutil.which("git"): return True
    print("\nGit isn't installed. Install it from git-scm.com (default options), reopen Command Prompt, and run this again.")
    sys.exit(1)

def sparse_clone(url, folder, paths):
    git_ok()
    if not os.path.exists(J(folder)):
        run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", url, folder])
    run(["git", "sparse-checkout", "set", "--no-cone"] + [f"/data/{p}/" for p in paths], cwd=J(folder))

print("1. Python libraries")
try:
    import numpy, scipy, sklearn  # noqa
    print("OK      numpy, scipy, scikit-learn")
except ImportError:
    run([PY, "-m", "pip", "install", "numpy", "scipy", "scikit-learn"])

print("\n2. Greek New Testament (SBLGNT)")
if need("sblgnt/", J("sblgnt")):
    git_ok(); run(["git", "clone", "--depth", "1", "https://github.com/morphgnt/sblgnt", "sblgnt"])

print("\n3. Chapter files for Stylo")
if need("corpus_nt_chapters/", J("corpus_nt_chapters")):
    run([PY, "make_corpus.py"])

print("\n4. English novels (the book's demo)")
if need("english_demo/corpus_whole/", J("english_demo", "corpus_whole")) and need("100_english_novels/", J("100_english_novels")):
    git_ok(); run(["git", "clone", "--depth", "1", "https://github.com/computationalstylistics/100_english_novels"])
    print("   (run english_demo with:  py -3.12 english_demo\\english_demo.py 100_english_novels\\corpus )")

print("\n5. Ignatius (genuine letters + later forgeries)")
base = "https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg1443/"
for name, work in (("g1.xml", "tlg001"), ("g2.xml", "tlg002")):
    if need(name, J(name)):
        for attempt in range(1, 6):        # retry: a download can be cut off by a brief network hiccup
            try:
                urllib.request.urlretrieve(f"{base}{work}/tlg1443.{work}.1st1K-grc1.xml", J(name + ".part"))
                os.replace(J(name + ".part"), J(name)); print("   downloaded", name); break
            except OSError as e:
                print(f"   attempt {attempt} failed ({e}); retrying"); time.sleep(3 * attempt)
        else:
            sys.exit(f"Could not download {name}. Check your connection and run setup_data.py again.")

print("\n6. Known Greek authors (for the error rates)")
if need("advanced/greek_reference.json", J("advanced", "greek_reference.json")):
    sparse_clone("https://github.com/PerseusDL/canonical-greekLit", "canonical-greekLit",
                 ["tlg0062", "tlg0551", "tlg0526", "tlg0060", "tlg0555"])
    sparse_clone("https://github.com/OpenGreekAndLatin/First1KGreek", "First1KGreek",
                 ["tlg0555", "tlg0018", "tlg0645", "tlg2018", "tlg2042", "tlg1271", "tlg1443", "tlg1622", "tlg1216", "tlg1766"])
    env = dict(os.environ, PERSEUS=J("canonical-greekLit"), FIRST1K=J("First1KGreek"))
    print("   building greek_reference.json (a minute or two)")
    subprocess.run([PY, "build_greek.py"], cwd=J("advanced"), env=env, check=True)

print("\n7. Letter writers (for the letter test)")
if need("advanced/letters_reference.json", J("advanced", "letters_reference.json")):
    sparse_clone("https://github.com/PerseusDL/canonical-greekLit", "canonical-greekLit",
                 ["tlg0062", "tlg0551", "tlg0526", "tlg0060", "tlg0555", "tlg2040", "tlg2003"])
    sparse_clone("https://github.com/OpenGreekAndLatin/First1KGreek", "First1KGreek",
                 ["tlg0555", "tlg0018", "tlg0645", "tlg2018", "tlg2042", "tlg1271", "tlg1443", "tlg1622", "tlg1216", "tlg1766", "tlg2200"])
    env = dict(os.environ, PERSEUS=J("canonical-greekLit"), FIRST1K=J("First1KGreek"))
    subprocess.run([PY, "build_letters.py"], cwd=J("advanced"), env=env, check=True)

print("\nAll inputs present. Next:  py -3.12 verify_writeup.py   (or run each script; see VERIFY.md)")
