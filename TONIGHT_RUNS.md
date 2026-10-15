# Quick checks added Oct 8-9 (run from this folder in Command Prompt)

All use the SBLGNT, accents stripped, 100 most frequent words (whole NT), Eder's Simple distance.
259 chapter samples (2 and 3 John combined, as in the book).

| Command | What it answers | Expected headline |
|---|---|---|
| `py -3.12 advanced\glom_test.py` | Do one author's chapters "glom together"? | Revelation 100%, Acts 89%, Luke 4-22 58%, Mark 38%, Romans 38%, core 4 Paul 53% (chance 19%) |
| `py -3.12 advanced\glom_noparallels.py` | Same, with parallel gospels removed | Mark 38% -> 88%; Matthew 86%; Luke all 24 92% (100% w/o Acts); John 100%; core-Paul chapters land in letters carrying Paul's name 41/51 |
| `py -3.12 advanced\nearest.py 1Th` | Closest chapters for any book (swap 1Th for Ro, Lk, Mk...) | 1 Thess 1-3 pair, 4-5 pair; outside matches 2 Cor 1, 8, Gal 6 |
| `py -3.12 advanced\frame_test.py` | Why Romans 1, 15, 16 group | Romans 15's closest: Ro 1, 1 Co 1, Php 1 (all letter openings) |
| `py -3.12 advanced\direction_test.py` | Does "Evangelion closer to Luke 4-22 than to Acts" show direction? | A cut-down Luke gives the same pattern (0.14-0.22 to Luke 4-22, 1.40 to Acts) |
| `py -3.12 advanced\book_level.py` | Whole books: do Luke and Acts come together? | Acts' closest = Luke (1.27); Luke's closest = Matthew (0.94), Mark, then Acts |
| `py -3.12 advanced\interp_test.py` | Remove suspected interpolations | Core-letter scores change by 0.04 or less (slow: ~10 min) |
| `py -3.12 advanced\date_vs_style.py` | Does style track date? | No: r = 0.16 (p = 0.24) across 9 dated Greek authors |

Needs: numpy (all), scipy (book_level tree + date test). Install once: `py -3.12 -m pip install numpy scipy`
