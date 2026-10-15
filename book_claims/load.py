"""Load SBLGNT (MorphGNT) into chapter-level word lists, the way a Stylo user would chunk it."""
import glob, os, re, unicodedata
from collections import OrderedDict

SRC = os.environ.get("SBLGNT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sblgnt"))

GROUP = {  # conventional scholarly grouping, used only to COLOR/score results, never as input
    "Mt": "Synoptic", "Mk": "Synoptic", "Lk": "Luke-Acts", "Ac": "Luke-Acts",
    "Jn": "Johannine", "1Jn": "Johannine", "2-3Jn": "Johannine", "Re": "Revelation",
    "Ro": "Paul (undisputed)", "1Co": "Paul (undisputed)", "2Co": "Paul (undisputed)",
    "Ga": "Paul (undisputed)", "Php": "Paul (undisputed)", "1Th": "Paul (undisputed)",
    "Phm": "Paul (undisputed)",
    "Eph": "Paul (disputed)", "Col": "Paul (disputed)", "2Th": "Paul (disputed)",
    "1Ti": "Pastorals", "2Ti": "Pastorals", "Tit": "Pastorals",
    "Heb": "Hebrews", "Jas": "Catholic", "1Pe": "Catholic", "2Pe": "Catholic", "Jud": "Catholic",
}


def strip(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return w.replace("ς", "σ")


def load(level="chapter", field="word"):
    """Return OrderedDict label -> list of tokens. field: 'word' (surface) or 'lemma'."""
    out = OrderedDict()
    for f in sorted(glob.glob(f"{SRC}/*-morphgnt.txt")):
        book = re.match(r"\d+-(\w+)-", os.path.basename(f)).group(1)
        if book in ("2Jn", "3Jn"):
            book = "2-3Jn"  # they merged these (ch. 7)
        for line in open(f, encoding="utf8"):
            ref, pos, parse, text, word, norm, lemma = line.split()
            ch = int(ref[2:4])
            tok = strip(norm if field == "word" else lemma)
            key = book if (level == "book" or book == "2-3Jn") else f"{book} {ch}"
            out.setdefault(key, []).append(tok)
    return out


def book_of(label):
    return label.split(" ")[0]
