"""
    Adds the texts supper.py needs, without re-running setup_data.py: Justin (tlg0645) and the Didache (tlg1311) to
    First1KGreek, and Tertullian's Against Marcion (stoa0275/stoa006) to canonical-latinLit. borrowing.py needs only
    sblgnt/. A folder already present is left alone; a missing checkout is cloned sparsely.

    Usage (from the kit folder):   python borrowing/fetch_texts.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
REPOS = {
    "First1KGreek": ("https://github.com/OpenGreekAndLatin/First1KGreek.git", ["/data/tlg0645/", "/data/tlg1311/"]),
    "canonical-latinLit": ("https://github.com/PerseusDL/canonical-latinLit.git", ["/data/stoa0275/stoa006/"]),
}


def main():
    for name, (url, folders) in REPOS.items():
        checkout = os.path.join(KIT, name)
        missing = []
        for folder in folders:
            if not os.path.isdir(os.path.join(checkout, folder.strip("/"))):
                missing.append(folder)
        if not missing:
            print(f"ok       {name}: all folders present")
            continue
        if not os.path.isdir(os.path.join(checkout, ".git")):
            if os.path.exists(checkout):
                sys.exit(f"'{checkout}' exists but is not a git checkout; add these folders by hand: {missing}")
            subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", url, checkout],
                           check=True)
            subprocess.run(["git", "sparse-checkout", "set", "--no-cone"] + missing, cwd=checkout, check=True)
        else:
            subprocess.run(["git", "sparse-checkout", "add"] + missing, cwd=checkout, check=True)
        for folder in folders:
            path = os.path.join(checkout, folder.strip("/"))
            print(f"{'ok      ' if os.path.isdir(path) else 'MISSING '} {path}")


if __name__ == "__main__":
    main()
