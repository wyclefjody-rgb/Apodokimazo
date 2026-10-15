# Figures, in the order of the argument

Remake them any time with `py -3.12 make_figures.py` (needs matplotlib: `py -3.12 -m pip install matplotlib`).
Trees 13, 14, 18 and 19 are converted from Stylo's PDFs in `output/` when available; otherwise run `Rscript run_stylo.R` and `Rscript consensus_check.R` first.

| # | Figure | What it shows | What to say |
|---|---|---|---|
| 01 | signal_vs_shuffled | 52% of chapters sit next to their own book; shuffled text 10%; function words alone 53% | "There's real signal, but half the chapters land next to another book. And it isn't theology words; grammar words alone give the same result." |
| 02 | stability | 41% of groupings pass Stylo's own consensus test; 22% of pairings survive 45 ordinary setting changes | "Most branches move when you nudge the settings, so one tree can't carry a big conclusion." |
| 03 | novels_by_length | Your English demo: 96% whole, 60% at 4,000, 27% at 700, 23% at 400 words | "Your validation works on whole books. Your Paul conclusions are at 400 words, where it gets 23%." |
| 04 | speech_chapters | 63% of Gospel discourse chapters match another discourse, vs about 20% by chance | "Speeches match speeches. That's genre, not a new author." |
| 05 | septuagint | Revelation 4-22 is the only text closer to the Septuagint; Luke 1-2, written in Greek, is next | "Sounding like the Septuagint doesn't prove translation. Luke 1-2 is next in line and you accept it was Greek." |
| 06 | blind_clustering | With names hidden: genre match 0.87 at 3 groups; author match 0.46 at 8 groups (shuffled 0.10) | "Left alone, the method finds genre first, then roughly the traditional authors." |
| 07 | blind_three_groups | 3 blind groups = letters (114/117), Revelation (22/24), narrative (113/118) | "This is what the first split is really about." |
| 08 | greek_attribution | 9 Greek authors, unseen works: at 400 words 60% (book method) to 79% (classifier) | "Against a big reference, short samples are OK. Your trees compare short against short." |
| 09 | greek_verification | Same author or not, two samples: AUC 0.75-0.83 at 400 words, better by 2,500 | "Deciding whether two chapters share an author is weak, even with forensic methods." |
| 10 | paul_verification | 1,500 words: core Paul 0.96 together, same as Acts' halves; Ignatius 0.37; 1 Peter 0.76, James 0.70 | "Paul's core letters look like one author. Fair caveat: 1 Peter and James are close too, so it supports, not proves." |
| 11 | tree_novels_whole | Your demo tree, whole novels | "Replicates your figure." |
| 12 | tree_novels_400_words | The same novels in 400-word pieces | "Same authors scatter at chapter length." |
| 13 | tree_acts_alone | Acts, one author, splits (roughly 1-12 / 13-28, with 22-26 apart) | "Why is this one author but Paul's split several?" |
| 14 | tree_whole_books | Whole books, your settings: Romans, 1-2 Corinthians, Galatians together | "At book length your own method groups Paul's core letters." |
| 15 | tree_greek_demo | Your Greek demo, replicated | "Replicates, but only against very different texts; add other NT books and Matthew's chapters have their own branch in 6-11% of runs." |
| 16 | tree_exhibit6_with_justin | Exhibit 6 plus Justin's Dialogue (one author) in blocks | "A known single work spreads about as much as 1 Clement." |
| 17 | tree_tiktok_test | The TikTok-style test, rerun | (from the TikTok exchange) |
| 18 | tree_consensus_all_chapters | Stylo's consensus tree for all chapters | "This is the version that only keeps stable branches." |
| 19 | tree_all_259_chapters | Every chapter, your settings (large) | "The full tree, not a selection." |
