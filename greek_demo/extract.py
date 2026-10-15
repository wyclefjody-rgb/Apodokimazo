"""Pull plain Greek text out of the Perseus / First1KGreek TEI files, cleaned the same way as the New Testament
(lowercase, accents removed, final sigma as σ). Notes, headings and apparatus are dropped; only Greek words are kept."""
import re, unicodedata, xml.etree.ElementTree as ET
NS = "{http://www.tei-c.org/ns/1.0}"
def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c)).replace("ς", "σ").replace("ϲ", "σ")
    return re.sub(r"[^α-ω]", "", w)
def text_of(el):
    for bad in list(el.iter()):
        for ch in list(bad):
            if ch.tag in (NS + "note", NS + "bibl", NS + "head", NS + "app", NS + "rdg", NS + "del", NS + "sic", NS + "ref", NS + "label"):
                bad.remove(ch)
    return [t for t in (norm(w) for w in re.findall(r"\S+", " ".join(el.itertext()))) if t]
def load(path, level=None, pick=None):
    """level: a textpart subtype such as 'book' or 'epistle'; pick: list of n values to keep (strings)."""
    root = ET.parse(path).getroot()
    body = root.find(f".//{NS}body")
    if level is None:
        return text_of(body)
    out = []
    for d in body.iter(NS + "div"):
        if d.get("subtype") == level and (pick is None or d.get("n") in pick):
            out += text_of(d)
    return out
def parts(path, level):
    root = ET.parse(path).getroot(); body = root.find(f".//{NS}body")
    return [(d.get("n"), text_of(d)) for d in body.iter(NS + "div") if d.get("subtype") == level]
