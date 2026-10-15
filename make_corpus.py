"""Build Stylo-ready corpus folders from the SBL Greek New Testament (MorphGNT).
Writes one .txt file per chapter, named Book_CC.txt (Stylo colours by the part before '_').
2 John and 3 John are merged, as the book did."""
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import glob, os, re, sys, unicodedata
SRC = sys.argv[1] if len(sys.argv) > 1 else "sblgnt"

def strip(w):
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if not unicodedata.combining(c)).replace("ς", "σ")

chapters = {}
for f in sorted(glob.glob(f"{SRC}/*-morphgnt.txt")):
    book = re.match(r"\d+-(\w+)-", os.path.basename(f)).group(1)
    if book in ("2Jn", "3Jn"): book = "23Jn"
    for line in open(f, encoding="utf8"):
        ref, pos, parse, text, word, norm, lemma = line.split()
        ch = 1 if book == "23Jn" else int(ref[2:4])
        chapters.setdefault((book, ch), []).append(strip(norm).replace("(", "").replace(")", ""))

def write(folder, keep):
    os.makedirs(folder, exist_ok=True)
    for (b, c), toks in chapters.items():
        if keep(b):
            open(f"{folder}/{b}_{c:02d}.txt", "w", encoding="utf8").write(" ".join(toks))

write("corpus_nt_chapters", lambda b: True)
write("corpus_acts", lambda b: b == "Ac")
# whole books, for the Paul test
os.makedirs("corpus_nt_books", exist_ok=True)
books = {}
for (b, c), t in chapters.items(): books.setdefault(b, []).extend(t)
for b, t in books.items():
    open(f"corpus_nt_books/{b}_book.txt", "w", encoding="utf8").write(" ".join(t))
print(len(chapters), "chapters,", len(books), "books written")
