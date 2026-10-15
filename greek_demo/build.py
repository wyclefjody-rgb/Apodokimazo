"""Build (1) their Chapter 7 Greek demo corpus and (2) their Exhibit 6 corpus, from open texts.
Their figure lists: Lucian (Symposium, Peregrinus, True Story), Appian (Spain, Punic, Illyrian), Josephus (Life, Against Apion,
War, War 1, Antiquities 1), Diodorus (1-5, 11-16), Origen (John commentary, Against Celsus, Oration, Letter to Africanus),
Justin (1 & 2 Apology), Eusebius (History 1, History 2, Ecclesiastical Theology), Clement of Alexandria (Protrepticus,
Paedagogus, Stromateis), Philo (On Virtues, Cherubim), Ignatius (Ephesians, Magnesians, Romans), Matthew 5-7, 1 Timothy 1-3.
Diodorus books 1-5 aren't in the open Perseus file, so only 11-16 is used."""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "noise_tests"))
from extract import load
from load import load as nt_load
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.environ.get("PERSEUS", os.path.join(HERE, "..", "canonical-greekLit")) + "/data/"
F = os.environ.get("FIRST1K", os.path.join(HERE, "..", "First1KGreek")) + "/data/"
nt = nt_load("chapter")
ntc = lambda b, c: nt[f"{b} {c}"]
DEMO = {
 "Lucian_Symposium": (C+"tlg0062/tlg015/tlg0062.tlg015.perseus-grc2.xml",), "Lucian_Peregrinus": (C+"tlg0062/tlg042/tlg0062.tlg042.perseus-grc2.xml",),
 "Lucian_TrueStory": (C+"tlg0062/tlg012/tlg0062.tlg012.perseus-grc2.xml",),
 "Appian_WarsSpain": (C+"tlg0551/tlg007/tlg0551.tlg007.perseus-grc2.xml",), "Appian_PunicWars": (C+"tlg0551/tlg009/tlg0551.tlg009.perseus-grc2.xml",),
 "Appian_IllyrianWars": (C+"tlg0551/tlg012/tlg0551.tlg012.perseus-grc2.xml",),
 "Josephus_Life": (C+"tlg0526/tlg002/tlg0526.tlg002.perseus-grc2.xml",), "Josephus_AgainstApion": (C+"tlg0526/tlg003/tlg0526.tlg003.perseus-grc2.xml",),
 "Josephus_War1": (C+"tlg0526/tlg004/tlg0526.tlg004.perseus-grc2.xml", "book", ["1"]),
 "Josephus_War2to7": (C+"tlg0526/tlg004/tlg0526.tlg004.perseus-grc2.xml", "book", ["2","3","4","5","6","7"]),
 "Josephus_Antiquities1": (C+"tlg0526/tlg001/tlg0526.tlg001.perseus-grc2.xml", "book", ["1"]),
 "Diodorus_Library11to16": (C+"tlg0060/tlg001/tlg0060.tlg001.perseus-grc4.xml", "book", ["11","12","13","14","15","16"]),
 "Origen_CommentaryJohn": (F+"tlg2042/tlg005/tlg2042.tlg005.1st1K-grc1.xml",), "Origen_AgainstCelsus": (F+"tlg2042/tlg001/tlg2042.tlg001.perseus-grc1.xml",),
 "Origen_Oration": (F+"tlg2042/tlg008/tlg2042.tlg008.perseus-grc1.xml",), "Origen_LetterAfricanus": (F+"tlg2042/tlg045/tlg2042.tlg045.1st1K-grc1.xml",),
 "Justin_FirstApology": (F+"tlg0645/tlg001/tlg0645.tlg001.1st1K-grc1.xml",), "Justin_SecondApology": (F+"tlg0645/tlg002/tlg0645.tlg002.perseus-grc2.xml",),
 "Eusebius_History1": (F+"tlg2018/tlg002/tlg2018.tlg002.1st1K-grc1.xml", "book", ["1"]),
 "Eusebius_History2": (F+"tlg2018/tlg002/tlg2018.tlg002.1st1K-grc1.xml", "book", ["2"]),
 "Eusebius_ChurchTheology": (F+"tlg2018/tlg009/tlg2018.tlg009.opp-grc1.xml",),
 "ClementAlexandria_Protrepticus": (F+"tlg0555/tlg001/tlg0555.tlg001.1st1K-grc1.xml",), "ClementAlexandria_Paedagogus": (F+"tlg0555/tlg002/tlg0555.tlg002.1st1K-grc1.xml",),
 "ClementAlexandria_Stromateis": (C+"tlg0555/tlg004/tlg0555.tlg004.perseus-grc2.xml",),
 "Philo_OnVirtues": (F+"tlg0018/tlg025/tlg0018.tlg025.1st1K-grc1.xml",), "Philo_Cherubim": (F+"tlg0018/tlg003/tlg0018.tlg003.1st1K-grc1.xml",),
 "Ignatius_Ephesians": (F+"tlg1443/tlg001/tlg1443.tlg001.1st1K-grc1.xml", "epistle", ["1"]),
 "Ignatius_Magnesians": (F+"tlg1443/tlg001/tlg1443.tlg001.1st1K-grc1.xml", "epistle", ["2"]),
 "Ignatius_Romans": (F+"tlg1443/tlg001/tlg1443.tlg001.1st1K-grc1.xml", "epistle", ["4"]),
}
def write(folder, texts):
    shutil.rmtree(folder, ignore_errors=True); os.makedirs(folder)
    for k, t in texts.items():
        open(f"{folder}/{k}.txt", "w", encoding="utf8").write(" ".join(t))
texts = {k: load(*v) for k, v in DEMO.items()}
for c in (5, 6, 7): texts[f"Matthew_{c}"] = ntc("Mt", c)
for c in (1, 2, 3): texts[f"1Timothy_{c}"] = ntc("1Ti", c)
write("corpus_their_demo", texts)
print({k: len(v) for k, v in texts.items()})

# Exhibit 6: 1 Clement in 5-chapter blocks as in the book, Barnabas in their blocks, and the other texts they list
from extract import parts
cl = dict(parts(F+"tlg1271/tlg001/tlg1271.tlg001.1st1K-grc1.xml", "chapter"))
ba = dict(parts(F+"tlg1216/tlg001/tlg1216.tlg001.opp-grc1.xml", "chapter"))
def block(d, a, b, extra=()): return sum([d.get(str(i), []) for i in list(extra) + list(range(a, b + 1))], [])
ex6 = {"1Clement_1-4andpreface": block(cl, 1, 4, ["preface"])}
for a, b in [(5,9),(10,14),(15,19),(20,24),(25,29),(30,34),(35,39),(40,44),(45,49),(50,54),(55,59),(60,65)]:
    ex6[f"1Clement_{a}-{b}"] = block(cl, a, b)
for a, b in [(1,3),(4,6),(7,9),(10,12),(13,15),(16,21)]:
    ex6[f"Barnabas_{a}-{b}"] = block(ba, a, b)
ex6["Polycarp_Epistle"] = load(F+"tlg1622/tlg001/tlg1622.tlg001.1st1K-grc1.xml")
ex6["Tatian_Greeks"] = load(F+"tlg1766/tlg001/tlg1766.tlg001.perseus-grc1.xml")
ex6["Justin_FirstApology"] = texts["Justin_FirstApology"]; ex6["Justin_SecondApology"] = texts["Justin_SecondApology"]
ex6["Justin_DialogueTrypho"] = load(F+"tlg0645/tlg003/tlg0645.tlg003.perseus-grc2.xml")
bk = nt_load("book")
ex6["James"] = bk["Jas"]; ex6["Hebrews"] = bk["Heb"]; ex6["Mark_13"] = ntc("Mk", 13)
ex6["Revelation_1"] = ntc("Re", 1); ex6["Revelation_2-3"] = ntc("Re", 2) + ntc("Re", 3)
write("corpus_exhibit6", ex6)
print({k: len(v) for k, v in ex6.items()})
