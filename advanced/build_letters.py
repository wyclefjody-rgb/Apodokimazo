"""Build letters_reference.json: Greek letter writers whose letters are not in dispute, for the letter test
(letters_test.py). Kept separate from greek_reference.json so the main results are untouched.

Each author's genuine letters are split into a few groups of consecutive letters; a group plays the part of a
"work", so a test passage always comes from letters the method has not seen.

Excluded as spurious, doubtful or not by the named writer:
  Basil (Deferrari's Loeb numbering), following the New Catholic Encyclopedia's list ("Basil, St."):
      8 (Evagrius), 10, 16, 38, 189 (Gregory of Nyssa), 39-45, 47, 50, 166-171, 197, 321, 360, 365-368,
      335-359 (the Libanius exchange: spurious or doubtful), 362 and 364 (written by Apollinaris, not Basil).
  Julian (Wright's Loeb): 74-83, which Wright says "with the possible exception of 81, are certainly not by Julian".
  Libanius: First1KGreek's Epistulae 1-839 (Foerster); the exchange with Basil is not in this range.
  Ignatius: the 7 genuine letters (middle recension). Pseudo-Ignatius: the 6 letters added in the long recension,
      usually taken to be by one later (4th-century) writer imitating Ignatius.

Run from the kit folder after setup_data.py:   py -3.12 advanced\\build_letters.py"""
import json, os, re, xml.etree.ElementTree as ET
from extract import parts, text_of, NS

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.environ.get("PERSEUS", os.path.join(HERE, "..", "canonical-greekLit")) + "/data/"
F = os.environ.get("FIRST1K", os.path.join(HERE, "..", "First1KGreek")) + "/data/"
p = lambda base, a, w, ed: f"{base}{a}/{w}/{a}.{w}.{ed}.xml"

BASIL_OUT = {8, 10, 16, 38, 189, *range(39, 46), 47, 50, *range(166, 172), 197, 321, 360, *range(365, 369),
             *range(335, 360), 362, 364}
JULIAN_OUT = set(range(74, 84))
GROUPS = 5   # groups of consecutive letters per author (Ignatius: one group per letter)

def num(n):
    """Letter number as int, or None for labels like 'frag_89b'."""
    return int(n) if n and n.isdigit() else None

def groups(letters, k=GROUPS):
    """Split a list of (number, words) into k groups of consecutive letters with about equal word counts."""
    total = sum(len(t) for _, t in letters); out, cur, size = [], [], 0
    for n, t in letters:
        cur.append((n, t)); size += len(t)
        if size >= total * (len(out) + 1) / k and len(out) < k - 1:
            out.append(cur); cur = []
    out.append(cur)
    return {f"letters_{g[0][0]}-{g[-1][0]}": sum((t for _, t in g), []) for g in out if g}

out = {"authors": {}, "excluded": {"Basil": sorted(BASIL_OUT), "Julian": sorted(JULIAN_OUT)}}

basil = [(n, t) for n, t in parts(p(C, "tlg2040", "tlg004", "perseus-grc2"), "letter") if num(n) not in BASIL_OUT]
out["authors"]["Basil"] = groups(basil)

def libanius(path):
    """Libanius's letters from the OCR'd First1KGreek edition, cleaned: each letter's number line (e.g. β')
    and the editor's addressee-and-date line (e.g. Ἐλεβίκῳ. (383 vel 387?)) are dropped, and words split
    across lines (φιλεῖ- σθαι) are rejoined. Without this, the edition itself makes Libanius easy to spot."""
    body = ET.parse(path).getroot().find(f".//{NS}body"); out = []
    for d in body.iter(NS + "div"):
        if d.get("subtype") != "letter": continue
        for el in list(d.iter(NS + "p"))[:2]:
            s = " ".join(el.itertext()).strip()
            if len(s.split()) <= 1 or re.search(r"\(\s*\d", s):     # number line, or addressee (date)
                for parent in d.iter():
                    if el in list(parent): parent.remove(el); break
        out.append((d.get("n"), text_of(d, join_hyphens=True)))
    return out

lib = libanius(p(F, "tlg2200", "tlg001", "1st1K-grc1"))
out["authors"]["Libanius"] = groups(lib)

jul = [(n, t) for n, t in parts(p(C, "tlg2003", "tlg013", "perseus-grc2"), "letter") if num(n) not in JULIAN_OUT]
out["authors"]["Julian"] = groups(jul, 4)
for w, name in (("tlg005", "To_the_Athenians"), ("tlg006", "To_Themistius")):   # his two long open letters
    out["authors"]["Julian"][name] = sum((t for _, t in parts(p(C, "tlg2003", w, "perseus-grc2"), "section")), [])

IGN = {"1": "Eph", "2": "Mag", "3": "Tral", "4": "Rom", "5": "Phld", "6": "Smyr", "7": "Pol"}
SPUR = {"13": "Mary-to-Ign", "1": "To-Mary", "4": "Tarsians", "5": "Philippians", "9": "Antiochenes", "10": "Hero"}
out["authors"]["Ignatius"] = {IGN[n]: t for n, t in parts(p(F, "tlg1443", "tlg001", "1st1K-grc1"), "epistle") if n in IGN}
out["authors"]["Ps-Ignatius"] = {SPUR[n]: t for n, t in parts(p(F, "tlg1443", "tlg002", "1st1K-grc1"), "epistle") if n in SPUR}

for a, ws in out["authors"].items():
    print(f"{a:12s} {sum(map(len, ws.values())):>7} words in {len(ws)} groups: " + ", ".join(f"{k} ({len(v)})" for k, v in ws.items()))
json.dump(out, open(os.path.join(HERE, "letters_reference.json"), "w", encoding="utf8"), ensure_ascii=False)
