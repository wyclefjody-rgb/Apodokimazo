# Can a writer's way of arguing be seen across languages, and does a known forger copy it? Predictions and rules

Written 2026-10-25, before rhetoric_across.py was written or run, and before the Latin text of Laodiceans was
obtained. Never edited; changes go in AMENDMENTS.md with a date.

## 1. Questions

1. **Do language-neutral features of argument survive translation?** The features are questions, answers to an
   imagined objector, "not ... but", conditionals, "for", "therefore", citation formulas, address and sentence
   length. Each is measured on the Greek of the 21 New Testament letters and on the Latin of the same letters (the
   Vulgate). If a feature carries a writer's habit, a letter should rank about the same in both languages.
2. **Does a known forger of Paul copy his words, his way of arguing, or both?** The Letter to the Laodiceans is a
   Latin forgery in Paul's name, made largely from phrases of Philippians and Galatians. It is compared with the
   Latin Paul.

## 2. Data

- **Greek:** SBLGNT (MorphGNT), the 21 letters Romans to Jude. The punctuated text is used for questions and
  sentence ends.
- **Latin:** the Clementine Vulgate as published in github.com/mborders/vulgata (commit 10a09891), the same 21
  letters.
- **Laodiceans:** the Latin text in J. B. Lightfoot's critical edition (Colossians and Philemon, 1875/1876), as
  reproduced at bible-researcher.com/laodiceans.html. The user copies the 20 verses into
  rhetoric_across/laodiceans.txt, one verse per line. The script prints the file's SHA-256 so the text used is on
  record.

Latin is normalised to lower case with j as i and v as u. Greek is normalised as in the rest of the kit.

## 3. Features

Each is a rate per 1,000 words, except sentence length.

| feature | Greek | Latin |
|---|---|---|
| questions | ";" (Greek question mark) | "?" |
| sentence length | words per sentence ending in "." or ";" | words per sentence ending in ".", "?" or "!" |
| "by no means" | μὴ γένοιτο | absit |
| "what then?" | τί οὖν | quid ergo, quid igitur |
| "not ... but" | sentences with οὐ / οὐκ / οὐχ / μή followed later by ἀλλά | sentences with non / nec / neque followed later by sed |
| conditionals | εἰ, ἐάν, εἴπερ | si, nisi |
| "for" | γάρ | enim, nam |
| "therefore" | οὖν, ἄρα, διό | ergo, igitur, itaque, ideo, ideoque |
| citation formula | γέγραπται, γραφή | scriptum, scriptura (all forms) |
| "you" | σύ / ὑμεῖς, all forms | tu, te, tibi, tui, uos, uobis, uestri, uestrum |
| "we" | ἡμεῖς, all forms | nos, nobis, nostri, nostrum |
| "brothers" | ἀδελφοί | fratres |

**Argument score** (used in part 2): the sum of the rates of questions, "by no means", "what then?", "not ... but",
conditionals, "for", "therefore" and citation formulas.

## 4. Tests and decision rules

**Part 1: does it survive translation?**
- **V1.** For each feature, the Spearman correlation between its Greek and Latin values across the 21 letters. A
  feature "survives" if the correlation is at least 0.7.
- **V2.** All features are standardised within each language. For each Latin letter, the nearest Greek letter is
  found (Euclidean distance on the surviving features). The match rate is the share of Latin letters whose nearest
  Greek letter is the same letter. Chance is 1 in 21 (about 5%). Part 1 counts as a success if the match rate is
  at least 50%.

If Part 1 fails, Part 2 is still run, but only the phrase measure (L1) is interpreted.

**Part 2: Laodiceans.**
- **L1, words.** The share of Laodiceans's 3-word sequences found anywhere in the Latin Paul (the 13 letters).
  Baseline: for each of Paul's 13 letters, cut into passages as long as Laodiceans, the share of each passage's
  3-word sequences found in the *other* 12 letters. Laodiceans is "pasted from Paul" if its share is above every
  passage of the baseline.
- **L2, argument.** Laodiceans's argument score, compared with every passage of Latin Paul as long as Laodiceans
  (consecutive, non-overlapping). Laodiceans "lacks Paul's argument" if its score is below the 5th percentile of
  those passages.

## 5. Predictions

1. At least 7 of the 12 features survive translation (V1). Questions, "by no means", "what then?", conditionals and
   "for" survive. Sentence length does not, because Greek and Latin editors punctuate differently.
2. V2: at least 50% of Latin letters match their own Greek letter.
3. L1: Laodiceans's share of 3-word sequences found in Paul is above every baseline passage (pasted from Paul).
4. L2: Laodiceans's argument score is below the 5th percentile of passages of Latin Paul of the same length.
5. Overall: the forger copied Paul's phrases but not his way of arguing.

## 6. Limits stated in advance

- The Latin of Paul is a translation. Part 1 measures how much of the writer survives it, but the translator's
  habits remain.
- Lightfoot's Laodiceans comes from a different Latin tradition from the Clementine Vulgate. Matching phrases are
  therefore undercounted, which works against prediction 3.
- Laodiceans is about 250 words. Small rates are noisy, which is why it is compared with passages of the same
  length, not with whole letters.
- Punctuation in both languages is by modern editors.
- Features and rules are by Claude (an AI model).
