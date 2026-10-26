"""
    Adds the three apocryphal Acts used by the slip-rate study to the kit's First1KGreek folder, without re-running
    setup_data.py: the Acts of John (tlg0317), the Acts of Thomas (tlg2038) and the Acts of Barnabas (tlg2949).

    Usage (from the kit folder):   python slip_rate/fetch_texts.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIRST1K = os.path.join(HERE, "..", "First1KGreek")
FOLDERS = ["/data/tlg0317/", "/data/tlg2038/", "/data/tlg2949/"]


def main():
    if not os.path.isdir(os.path.join(FIRST1K, ".git")):
        sys.exit(f"'{FIRST1K}' is not a git checkout. Run setup_data.py first.")
    subprocess.run(["git", "sparse-checkout", "add"] + FOLDERS, cwd=FIRST1K, check=True)
    for folder in FOLDERS:
        path = os.path.join(FIRST1K, folder.strip("/"))
        print(f"{'ok  ' if os.path.isdir(path) else 'MISSING'} {path}")


if __name__ == "__main__":
    main()
