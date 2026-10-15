"""Build the Greek reference collection used to measure error rates: 9 Greek prose authors of the 1st c. BCE - 4th c. CE
whose authorship is not in dispute, 3-7 works each, plus the early Christian letters used as comparisons.
Reads the Perseus canonical-greekLit and First1KGreek clones (see greek_demo/README.md; extra folders are listed below)."""
import json, os, sys
from extract import load
C = os.environ.get("PERSEUS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "canonical-greekLit")) + "/data/"
F = os.environ.get("FIRST1K", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "First1KGreek")) + "/data/"
p = lambda base, a, w, ed: f"{base}{a}/{w}/{a}.{w}.{ed}.xml"
WORKS = {
 "Lucian":   [p(C,"tlg0062",w,"perseus-grc2") for w in ("tlg012","tlg015","tlg022","tlg031","tlg038","tlg053","tlg034")],
 "Appian":   [p(C,"tlg0551",w,"perseus-grc2") for w in ("tlg007","tlg009","tlg013","tlg014","tlg017")],
 "Josephus": [p(C,"tlg0526",w,"perseus-grc2") for w in ("tlg001","tlg002","tlg003","tlg004")],
 "Diodorus": [p(C,"tlg0060","tlg001",e) for e in ("perseus-grc4","perseus-grc5","perseus-grc6")],
 "ClementAlex": [p(F,"tlg0555","tlg001","1st1K-grc1"), p(F,"tlg0555","tlg002","1st1K-grc1"), p(C,"tlg0555","tlg004","perseus-grc2"), p(F,"tlg0555","tlg006","1st1K-grc1")],
 "Philo":    [p(F,"tlg0018",w,"1st1K-grc1") for w in ("tlg001","tlg003","tlg011","tlg020","tlg022","tlg030","tlg031")],
 "Justin":   [p(F,"tlg0645","tlg001","1st1K-grc1"), p(F,"tlg0645","tlg003","perseus-grc2")],
 "Eusebius": [p(F,"tlg2018",w,"1st1K-grc1") for w in ("tlg002","tlg005","tlg007","tlg020","tlg022")],
 "Origen":   [p(F,"tlg2042","tlg001","perseus-grc1"), p(F,"tlg2042","tlg005","1st1K-grc1"), p(F,"tlg2042","tlg007","perseus-grc1"),
              p(F,"tlg2042","tlg008","perseus-grc1"), p(F,"tlg2042","tlg009","opp-grc1")],
}
OTHER = {  # early Christian texts used only as comparisons / impostors
 "1Clement": p(F,"tlg1271","tlg001","1st1K-grc1"), "Ignatius": p(F,"tlg1443","tlg001","1st1K-grc1"),
 "Polycarp": p(F,"tlg1622","tlg001","1st1K-grc1"), "Barnabas": p(F,"tlg1216","tlg001","opp-grc1"),
 "Tatian": p(F,"tlg1766","tlg001","perseus-grc1"),
}
CAP = 40000   # words kept per work (the start of very long works), to keep run time down
out = {"authors": {}, "other": {}}
for a, fs in WORKS.items():
    out["authors"][a] = {os.path.basename(f).split(".")[1] + "_" + f.split(".")[-2]: load(f)[:CAP] for f in fs}
    print(a, {k: len(v) for k, v in out["authors"][a].items()})
for k, f in OTHER.items():
    out["other"][k] = load(f); print(k, len(out["other"][k]))
json.dump(out, open("greek_reference.json", "w", encoding="utf8"), ensure_ascii=False)
