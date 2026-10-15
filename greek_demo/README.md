# Their Chapter 7 Greek demo and Exhibit 6, rebuilt

Rebuilds the book's Greek demo (Lucian, Appian, Josephus, Diodorus, Origen, Justin, Eusebius, Clement of Alexandria, Philo, Ignatius, Matthew 5-7, 1 Timothy 1-3) and Exhibit 6 (1 Clement in 5-chapter blocks, Barnabas, Polycarp, Tatian, Justin, James, Hebrews, Mark 13, Revelation 1 and 2-3) from open Greek texts, then adds fair versions and a single-author control (Justin's Dialogue in 560-word blocks).

**1. Download the two open Greek collections** (from the kit folder, one time, about 2 minutes):

    git clone --depth 1 --filter=blob:none --sparse https://github.com/PerseusDL/canonical-greekLit.git
    cd canonical-greekLit && git sparse-checkout set data/tlg0062 data/tlg0551 data/tlg0526 data/tlg0060 data/tlg0555 data/tlg1216 data/tlg2018 && cd ..
    git clone --depth 1 --filter=blob:none --sparse https://github.com/OpenGreekAndLatin/First1KGreek.git
    cd First1KGreek && git sparse-checkout set data/tlg0018 data/tlg0555 data/tlg0645 data/tlg1216 data/tlg1271 data/tlg1443 data/tlg1622 data/tlg1766 data/tlg2018 data/tlg2042 && cd ..

**2. From inside `greek_demo`:**

    python build.py        (builds corpus_their_demo and corpus_exhibit6)
    python analyze.py      (their demo, the fair version with 6 NT books, and the Justin control)
    Rscript trees.R        (the trees, with 100 MFW and Eder's Delta)

Expected: their demo replicates (Matthew and 1 Timothy on their own branches). With Mark, Luke, Romans and 1 Corinthians added, Matthew's 3 chapters form their own branch in about 1 run in 10. Justin's Dialogue, one author, spreads over 5 branches, and 1 Clement over 3.

Not included: Diodorus books 1-5 and Aristides aren't in the open files.
