# Methods: exactly what this kit used, and why

This answers the questions you asked of the book, applied to this kit: which text, which files, which settings, and why. Everything below is in the kit and can be rerun. Random choices use fixed seeds, so you get the same numbers every time.

## The main rule

**Copy their setup exactly, then change one thing at a time.** The goal isn't to find the "best" settings. It's to use the book's own settings and see what happens when you test them. Where the book doesn't say what it did, the choice below is the neutral default, and it's stated.

---

## 1. Input text

| | Used | Why |
|---|---|---|
| Greek New Testament | **SBL Greek New Testament** (SBLGNT, Society of Biblical Literature, 2010), from the MorphGNT project: github.com/morphgnt/sblgnt | A standard critical edition, free, and word-tagged. The book never names its edition. |
| Word form | MorphGNT's "normalized word" column: lowercase, accents and breathing marks removed, final ς written as σ | Stylo counts words as written, so accents would split one word into several. This is the standard cleanup for Greek stylometry. |
| Greek Old Testament | **Rahlfs Septuagint (1935)**: github.com/eliranwong/LXX-Rahlfs-1935. Books over 1,500 words, cleaned the same way. | The standard Septuagint edition, and free. Used only for the Revelation / Luke 1–2 test. |
| English novels | Stylo's own **"100 English novels"** collection: github.com/computationalstylistics/100_english_novels. The 22 novels shown in the book's English figure. | It's the collection their figure uses, with the same file names. Harry Potter left out because it's under copyright. |
| Second English check | Stylo's built-in `novels` sample (Austen and the three Brontë sisters, 9 novels) | Comes with Stylo itself, so anyone can check it. |

**Segments.** New Testament: 259 texts, one per standard chapter. 2 and 3 John are merged into one text, as the book did. Nothing else is merged or split. Whole-book runs use 26 texts. The book also split some texts differently (Romans by Robert Price's divisions, 1 Clement in 5-chapter blocks, 2 Corinthians into proposed letters). Those splits weren't copied, because the book doesn't list all its boundaries. `make_corpus.py` writes every segment as a separate file, so anyone can inspect them.

## 2. Settings

| Setting | Used | Why |
|---|---|---|
| Features | Single words (1-grams) | Printed on their figures and confirmed in their email to a critic. |
| Most frequent words | 100 | Printed on their figures: "100 MFW." |
| Culling | 0% | Printed on their figures: "Culled @ 0%." |
| Distance | **Eder's Simple** | Printed on their figures. It's the Manhattan distance between square-rooted word frequencies, as Stylo calculates it. |
| Tree building | Ward linkage (`ward.D`) | Stylo's default. The book doesn't say otherwise. |
| Software | Stylo 0.7.71 in R 4.3; Python 3 with numpy and scipy for the extra tests | Stylo because it's what they used. Python was checked against it: both give 52% same-book matches. |

## 3. Each test, and why it was chosen

| Test | What was done | Why |
|---|---|---|
| **Signal vs noise** | Same-book closest match on the real text, then again after shuffling all words randomly (20 runs) | Shows how much of the tree is real signal and how much chance would produce anyway. |
| **Sample size** | 10 books over 4,000 words. Half of each book is the reference; a random sample from the other half is matched to the closest reference. 150 to 2,000 words, 40 trials each. | Measures accuracy at their chapter lengths, on an easy task where the answer is known. |
| **Stability** | 45 setting combinations: 50/100/200/300/500 words × Classic Delta, Cosine Delta, Eder's Simple × Ward, average, complete linkage | Checks whether groupings survive ordinary changes. Their Final Disclaimer asks for this. |
| **Consensus tree** | Stylo's own bootstrap consensus: 100 to 1,000 words in steps of 100, 50% rule | Stylo's built-in check for whether a grouping is stable. |
| **Acts control** | Acts alone, their settings | A single-author book, to see whether the method splits one author. |
| **Paul** | The 7 undisputed letters compared against every possible group of New Testament letters, as whole letters and as 1,400-word samples (200 random draws) | Tests the "group of authors" claim. Equal-length samples stop long letters from looking alike just because they're long. |
| **English demo** | Their 22 novels whole, then 4 random pieces per novel at 4,000, 700 and 400 words, 20 repetitions. A piece counts as correct if its closest match is **a different book by the same author**. Authors with only one book in a comparison (Emily Brontë in the Stylo sample, or Rowling if you add Harry Potter) are left out of the scoring because they have nothing to match. Chance is about 7%. | Their own validation, rerun at their chapter lengths. Requiring a different book stops pieces from matching just because they share characters or a plot. |
| **Speech chapters** | Closest matches for Mark 13, Matthew 24, Luke 21 and John 14–17. How often speech chapters match other speech chapters versus chance. | Tests whether their "separate author" sections are really a genre effect. |
| **Septuagint** | Revelation 1, 2–3 and 4–22, and Luke 1–2, compared with Septuagint books and New Testament books | Tests their "translated from Hebrew" reasoning against a passage they say was written in Greek. |

## 4. Limits, stated up front

- **Not their exact run.** Different Greek edition possibly, and some of their splits aren't copied. Their specific trees may differ. The sample-size, stability and single-author tests are about how the method behaves, so they don't depend on these choices.
- **Same method, with the same weaknesses.** At 400 words these results are noisy too. That's the point being tested, but it applies to the kit's chapter-level numbers as well.
- **The "speech chapter" list was chosen by hand** (chapters that are mostly one long speech by Jesus). Someone could pick a different list.
- **Distances depend on length.** In the Septuagint test, Luke 1–2 (2,035 words) is shorter than Revelation 4–22 (8,218 words). Shorter texts usually come out *more* distant, so Luke 1–2 being just as close makes the point stronger, not weaker.
- **The 15-finding verdicts are a judgment**, based on these tests and on the historical sources cited. The numbers are reproducible; the labels are an interpretation.
- **Tokenizing differs slightly.** The English novels were split into words with a simple lowercase letters-and-apostrophes rule, not Stylo's own tokenizer. The whole-novel tree still matches the book's figure.

## 5. Where each result comes from

| Result | File |
|---|---|
| 52% same-book, consensus 41% / 12% / 63, Acts split | `run_stylo.R`, `consensus_check.R` |
| Sample size, stability, shuffled text | `noise_tests/analysis.py`, `noise_tests/chunk.py` |
| Paul | `paul_test.py` |
| Stylo sample novels, Matthew vs Mark, top-100 words | `book_claims/their_claims.py` |
| Speech chapters | `book_claims/speech_test.py` |
| Septuagint | `book_claims/lxx_test.py` |
| English demo and trees | `english_demo/english_demo.py`, `english_demo/trees.R` |

Run all of it with `python run_all.py` (Windows) or `python3 run_all.py` (Mac).
