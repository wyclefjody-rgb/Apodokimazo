"""
    Downloads the Clementine Vulgate used by rhetoric_across (github.com/mborders/vulgata, MIT licence) and extracts
    its New Testament into rhetoric_across/vulgate/new_testament.json. Nothing else in the kit is touched.

    Usage (from the kit folder):   python rhetoric_across/fetch_texts.py
"""
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "vulgate")
REPO = "https://github.com/mborders/vulgata.git"
COMMIT = "10a09891b1721c41e39bfdb6322048e01fb4e15c"


def main():
    if os.path.exists(os.path.join(TARGET, "new_testament.json")):
        print(f"ok   {TARGET} already has new_testament.json")
        return
    work = tempfile.mkdtemp()
    try:
        clone = os.path.join(work, "vulgata")
        subprocess.run(["git", "clone", "--quiet", REPO, clone], check=True)
        subprocess.run(["git", "checkout", "--quiet", COMMIT], cwd=clone, check=True)
        os.makedirs(TARGET, exist_ok=True)
        with tarfile.open(os.path.join(clone, "bible.tar.gz")) as archive:
            member = None
            for item in archive.getmembers():
                if os.path.basename(item.name) == "new_testament.json" and item.isfile():
                    member = item
            if member is None:
                sys.exit("new_testament.json not found in bible.tar.gz")
            source = archive.extractfile(member)
            with open(os.path.join(TARGET, "new_testament.json"), "wb") as out:
                shutil.copyfileobj(source, out)
        print(f"ok   {os.path.join(TARGET, 'new_testament.json')} (vulgata commit {COMMIT[:8]})")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
