"""
    Adds the Attic orators attic_hands needs to the kit's canonical-greekLit checkout, without re-running
    setup_data.py. A folder already present is left alone; a missing checkout is cloned sparsely (only the folders
    listed here).

    Usage (from the kit folder):   python attic_hands/fetch_texts.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
REPOS = {
    "canonical-greekLit": ("https://github.com/PerseusDL/canonical-greekLit.git",
                           ["/data/tlg0014/", "/data/tlg0540/", "/data/tlg0017/", "/data/tlg0028/", "/data/tlg0027/",
                            "/data/tlg0026/", "/data/tlg0010/tlg001/", "/data/tlg0010/tlg002/", "/data/tlg0010/tlg003/",
                            "/data/tlg0010/tlg004/", "/data/tlg0010/tlg005/", "/data/tlg0010/tlg006/"]),
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
