# Stronger methods: error rates, authorship verification and likelihood ratios

Needs the two Greek collections from `greek_demo/README.md`, plus these extra folders in the sparse checkouts:

    cd canonical-greekLit && git sparse-checkout add data/tlg0062 data/tlg0551 data/tlg0526 data/tlg0060 data/tlg0555 && cd ..
    cd First1KGreek && git sparse-checkout add data/tlg0018 data/tlg0555 data/tlg0645 data/tlg1216 data/tlg1271 data/tlg1443 data/tlg1622 data/tlg1766 data/tlg2018 data/tlg2042 && cd ..

Then, from inside `advanced` (set PERSEUS and FIRST1K to the two folders if they aren't in the default place):

    python build_greek.py      builds greek_reference.json (9 Greek authors, 3-7 works each, plus 1 Clement, Ignatius, Barnabas, Tatian)
    python calibrate.py        error rates on the 9 authors (about 4 min)
    python calibrate.py ClementAlex Justin Eusebius Origen Philo     the harder version: 5 Jewish and Christian writers
    python nt_apply.py         Paul, controls and comparisons at 400 and 1,500 words (about 2 min)

What each method is:
- **Book method**: 100 most frequent words, Eder's Simple distance (Stylo).
- **Cosine**: 300 words + 500 three-letter sequences, z-scored, cosine similarity (a "Cosine Delta" with more features).
- **Classifier**: logistic regression on the same 800 features.
- **General Impostors** (Koppel & Winter 2014): how often two samples are closer to each other than to any of 20 "impostor" samples by other writers, over 60 random halves of the features. 0 to 1.
- **Likelihood ratio**: the cosine score converted into "how many times more likely if same author," calibrated on the known Greek authors (logistic-regression calibration, the standard score-based approach), with Cllr as the quality check (0 perfect, 1 uninformative).

Every test sample is taken from a work that the method's reference material doesn't include.
