# Amendments to PREDICTIONS.md (early_witnesses)

PREDICTIONS.md is never edited (SHA-256 5eb2ae9b847b9122aca62d591e5f6187e5e060ef486a139fcc34d0221ae79acb).

## 1. 2026-10-25: after the first run. The echo rule catches stock phrases; a rare-word check is added

The rule of section 3 found echoes of the classes outside A in the witnesses, but just as many in the controls. Most
of them are stock Christian phrases that happen not to occur in the LXX or elsewhere in the New Testament: "the
love of God", "for I do not want you to be ignorant", "to the glory of God", "our Saviour Jesus Christ". Hermas and
Barnabas, which are not thought to use Paul much, score as high as the witnesses.

So the mechanical verdicts are reported as they fall, with their weakness stated:
- Prediction 3 is "met" by the rule, but on stock phrases only. It is not taken as evidence that any witness knew
  the passages missing from Marcion's edition.
- Prediction 1 fails as measured. The rate per 1,000 words of Paul does not allow for the witnesses' very
  different lengths (Polycarp 1,580 words, Hermas 28,547).

Added as exploratory (RESULTS.md section 4), after seeing the results: the same echoes, kept only if they contain at
least one word that occurs at most 10 times in the New Testament and the LXX together, counted per 10,000 words of
the witness. This filter was chosen after the first run, so its results are exploratory, not tests.

## 2. 2026-10-25: what the test can and cannot show

Exact 4-word matching misses allusion. 1 Clement 47 names 1 Corinthians and summarises it, but in its own words, so
the rule finds little of it. A "no" from this test therefore says little. The better instrument for the question in
section 1 is a hand-coded list of allusions, such as the one in *The New Testament in the Apostolic Fathers* (Oxford
Society of Historical Theology, 1905; Gregory and Tuckett, 2005), classified against Marcion's gaps. That would be a
separate, pre-registered study.

## 3. 2026-10-27: allusion test (ALLUSIONS_PREDICTIONS.md), set after coding, before the tally was run

ALLUSIONS_PREDICTIONS.md is never edited (SHA-256 166b48c2ad69f2570598a2372007a4bd12d2261894c578e1577bab9c342cf513).
These choices were made while coding the 1905 entries, so after the entries had been seen, but before allusions.py
was written or run.

- **"Graded" in prediction 4** means grades a to d. Entries printed as "Unclassed" are listed but not counted. The
  a-c version is reported beside it.
- **The pool for prediction 4** is the writer's entries citing at least one of the ten letters of Marcion's
  collection (classes A, B, C). Entries citing only the Pastorals are left out, because class B's share is a share
  of the ten letters' words.
- **Class B's share** is measured from SBLGNT: 6.8%, not the "about 6%" of the predictions. The threshold is a
  third of the measured share (2.3%). With 6% (threshold 2.0%) the verdicts are the same.
- **Cross-references.** Where the committee lists an entry under a second letter only to say "see under" another
  entry of the same writer (Polycarp 70 and 71), it is coded x and not counted twice. Its passages are already in
  the entry it points to.
- **Changed phrases.** Of the entries touching them, only Hermas (6) on Ephesians 2:20 has the missing words
  ("prophets"), so it is coded class B. Ignatius (23) on 1 Corinthians 15:45, Ignatius (32) on Ephesians 2:20 and
  Ignatius (33) on Ephesians 3:9 do not, so they are class A.
- **Exploratory, not a test:** an expected count for each writer that allows for which letters the writer uses.
  Each entry's chance of falling in class B is class B's share of the words of the letters it cites. Nearly all of
  class B is in Romans, so the plain 6.8% overstates what to expect from a writer who seldom uses Romans.
