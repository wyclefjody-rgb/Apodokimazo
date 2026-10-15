"""Pull plain Greek text out of the Perseus / First1KGreek TEI files, cleaned the same way as the New Testament
(lowercase, accents removed, final sigma as σ). Notes, headings and apparatus are dropped; only Greek words are kept."""
import re, unicodedata, xml.etree.ElementTree as ET
NS = "{http://www.tei-c.org/ns/1.0}"
def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c)).replace("ς", "σ").replace("ϲ", "σ")
    return re.sub(r"[^α-ω]", "", w)
def text_of(el, join_hyphens=False):
    """Words of an element. join_hyphens: rejoin words split across lines in OCR texts (e.g. φιλεῖ- σθαι)."""
    drop = (NS + "note", NS + "bibl", NS + "head", NS + "app", NS + "rdg", NS + "del", NS + "sic", NS + "ref", NS + "label")
    for parent in list(el.iter()):
        kids = list(parent)
        for i, ch in enumerate(kids):
            if ch.tag in drop:
                # keep the text that FOLLOWS the removed tag (ElementTree stores it as ch.tail)
                if ch.tail:
                    prev = kids[i - 1] if i > 0 else None
                    if prev is not None and prev in list(parent):
                        prev.tail = (prev.tail or "") + " " + ch.tail
                    else:
                        parent.text = (parent.text or "") + " " + ch.tail
                parent.remove(ch)
    s = " ".join(el.itertext())
    if join_hyphens:
        s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    return [t for t in (norm(w) for w in re.findall(r"\S+", s)) if t]
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
