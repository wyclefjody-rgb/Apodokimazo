"""
    Adds the texts letter_form needs to the kit's three Perseus / First1KGreek checkouts, without re-running
    setup_data.py. A folder already present is left alone; a missing checkout is cloned sparsely (only the folders
    listed here).

    Usage (from the kit folder):   python letter_form/fetch_texts.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
REPOS = {
    "First1KGreek": ("https://github.com/OpenGreekAndLatin/First1KGreek.git",
                     ["/data/tlg1443/", "/data/tlg1271/", "/data/tlg1622/", "/data/tlg0037/", "/data/tlg0041/",
                      "/data/tlg0053/", "/data/tlg0055/", "/data/tlg0623/", "/data/tlg0636/", "/data/tlg0637/",
                      "/data/tlg1325/", "/data/tlg1367/", "/data/tlg1803/", "/data/tlg0640/"]),
    "canonical-greekLit": ("https://github.com/PerseusDL/canonical-greekLit.git",
                           ["/data/tlg0081/", "/data/tlg0007/tlg111/", "/data/tlg0074/tlg004/",
                            "/data/tlg0545/tlg003/", "/data/tlg0638/tlg006/"]),
    "canonical-latinLit": ("https://github.com/PerseusDL/canonical-latinLit.git",
                           ["/data/phi0474/phi056/", "/data/phi0474/phi057/", "/data/phi1017/phi015/",
                            "/data/phi1318/phi001/"]),
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
