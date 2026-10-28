"""
    Adds the letters real_letters needs (Pliny, Cicero to Atticus, Seneca) to the kit's canonical-latinLit
    checkout, without re-running
    setup_data.py. A folder already present is left alone; a missing checkout is cloned sparsely (only the folders
    listed here).

    Usage (from the kit folder):   python real_letters/fetch_texts.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
REPOS = {
    "canonical-latinLit": ("https://github.com/PerseusDL/canonical-latinLit.git",
                           ["/data/phi1318/", "/data/phi0474/", "/data/phi1017/"]),
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
