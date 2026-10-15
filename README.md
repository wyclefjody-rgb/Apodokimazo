# Christ Before Jesus: stylometry re-run kit

## Quick start (Windows or Mac)

1. **Install Python 3** from python.org. On Windows, tick "Add Python to PATH" during setup.
2. **Install R** from cran.r-project.org. RStudio is optional, but it's what the book uses.
3. **Install git** from git-scm.com. This is optional: it downloads the two extra text collections automatically.
4. **Install the Python libraries.** Open Terminal (Mac) or Command Prompt (Windows) and run:
   `pip install numpy scipy scikit-learn`
5. **Install Stylo.** Open R and run:
   `install.packages(c("stylo", "ape"))`
6. **Run everything.** In Terminal or Command Prompt, go to this folder (`cd` followed by the folder path), then run:
   - Windows: `python run_all.py`
   - Mac: `python3 run_all.py`

It takes about 5 minutes. Every result prints on screen, and the tree pictures are saved in `output/` and `english_demo/`.

**To see the trees the way the book does,** open R and run `library(stylo); stylo()`. That opens Stylo's point-and-click window. Point it at a corpus folder, for example `corpus_nt_chapters` (created by run_all) or `english_demo/corpus_400`, then choose Cluster Analysis, 100 MFW, culling 0 and Eder's Simple distance.

**If git isn't installed,** download these two as ZIP files from GitHub, unzip them into this folder, and rename the folders exactly as shown:
- https://github.com/eliranwong/LXX-Rahlfs-1935 → `lxx`
- https://github.com/computationalstylistics/100_english_novels → `100_english_novels`

The questions to ask, with the evidence for each, are in **QUESTIONS.md**. What this kit used and why (the same questions, answered for this kit) is in **METHODS.md**.

---

This kit re-runs the stylometry from *Christ Before Jesus* (Britt and Wingo, 2024) on the Greek New Testament, then tests how reliable it is. Everything here is free software, and every number on the write-up page comes from these scripts.

## What's inside

| File | What it does |
|---|---|
| `sblgnt/` | The SBL Greek New Testament with word tags (MorphGNT project, free licence). |
| `make_corpus.py` | Turns the Greek text into one file per chapter, in the format Stylo reads. 2 and 3 John are merged, as the book did. |
| `run_stylo.R` | Runs **Stylo itself** with the settings the authors gave a critic by email: 100 most frequent words, single words, Eder's Simple distance, no culling. Makes their kind of tree, the consensus tree, the Acts control and a whole-book tree. |
| `consensus_check.R` | Counts how many of the tree's groupings survive Stylo's own stability check. |
| `paul_test.py` | Tests whether Paul's letters look like one writer or a group. |
| `noise_tests/` | Python versions of the noise tests: sample size, 45 setting combinations, shuffled-text null, Acts and Luke. |
| `run_all.py` | Runs everything in order, on Windows or Mac (`run_all.sh` does the same on Mac/Linux). |

## How to run it

You need Python 3 and R.

1. Install the Python libraries:
   `pip install numpy scipy scikit-learn`
2. Install Stylo in R:
   `install.packages("stylo")` (this also installs `ape`, which the consensus check uses)
3. From this folder, run:
   `bash run_all.sh`

It takes a few minutes. Results print to the screen, and trees (PDF) and tables go in `output/`.

To see the trees the way the authors did, you can also open Stylo's point-and-click window in R with `library(stylo); stylo()`. Point it at `corpus_nt_chapters`, pick "Cluster Analysis", 100 MFW and "Eder's Simple".

## What to expect

- **Stylo nearest-neighbour check:** 52% of chapters have their closest match in the same book.
- **Consensus check:** of 257 groupings in the 100-word tree, 105 (41%) survive the 50% rule, 31 (12%) appear in all 10 runs, and 63 chapters have no stable place at all.
- **Acts control:** Stylo splits Acts into chapters 1–7 and 9–12 versus 8 and 13–28.
- **Sample size:** about 79% correct at 500 words, 94% at 2,000 words (10 books, easy test).
- **Paul:** whole letters group tightly (Romans, 1 and 2 Corinthians and Galatians pick each other as closest). At equal 1,400-word samples the evidence is weaker: those four usually still pick each other, but Philippians and 1 Thessalonians do not stand out.

Small differences are normal if you change the Greek edition or how words are cleaned up.

## Limits

The authors never published their input files, so this is a reconstruction from what they told critics. If they used another Greek edition or split chapters differently, their exact tree would differ. The sample-size, stability and Acts tests are about how the method behaves, so they apply either way.

## Tests of the book's own claims (`book_claims/`)

Run from inside `book_claims/`:

- `python3 their_claims.py`: Stylo's sample English novels cut to New Testament chapter sizes (whole novel 100%, 700 words 58%, 400 words 43% correct author, not counting Emily Brontë, who has only one novel); how often Matthew's chapters match Matthew versus the parallel chapter in Mark (36% match Matthew); which "theological" words are in the top 100.
- `python3 speech_test.py`: Mark 13 and John 14–17. Their closest matches are other speeches and parallels (speech chapters match speech chapters 63% of the time versus about 20% by chance).
- `python3 lxx_test.py`: Revelation 4–22 and Luke 1–2 against the Greek Septuagint. First download the Septuagint into the kit folder:
  `git clone https://github.com/eliranwong/LXX-Rahlfs-1935.git lxx`

## The book's English demo, rerun (`english_demo/`)

Their Chapter 7 English figure uses 22 novels from Stylo's public collection plus one Harry Potter book. To rerun it:

1. `git clone https://github.com/computationalstylistics/100_english_novels.git`
2. From inside `english_demo/`: `python3 english_demo.py ../100_english_novels/corpus`
3. For the trees: `Rscript trees.R`

Expected: whole novels 95% correct author, 4,000 words 60%, 700 words 27%, 400 words 23% (chance is about 7%).

**Harry Potter:** it's still under copyright, so it isn't included. But, it will get cut into pieces the same way as the other novels.
