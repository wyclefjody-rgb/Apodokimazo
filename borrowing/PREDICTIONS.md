# Who borrowed from whom? Predictions and rules (borrowing, with the Last Supper test)

Written 2026-10-24, before borrowing.py and supper.py were written or run. Never edited; changes go in
AMENDMENTS.md with a date. One exception is declared here: Justin's Last Supper quotation (First Apology 66.3) was
read while the source files were being located, before this file was written. Prediction S4 below is therefore a
description, not a prediction.

## 1. Questions

1. **Calibrated borrowing test.** Can simple measures tell known literary borrowing from shared church language
   among the New Testament letters? If so, where do the claimed cases fall?
   - 1 Peter and Hebrews (Carrier, citing Elizabeth Meyers's analysis);
   - 1 Peter with Romans and Ephesians (the usual scholarly claim);
   - Mark 12:13-17 ("render to Caesar") with Romans 13:1-7 (Carrier: Mark turns Paul's teaching into a saying of
     Jesus).
2. **The Last Supper.** How Luke 22, Mark 14, Matthew 26 and 1 Corinthians 11 share their wording, with Justin, the
   Didache and Marcion's gospel beside them.

## 2. Measures for whole texts (borrowing.py)

Data: SBLGNT with MorphGNT lemmas. Units are whole books.
- **Rare shared words:** lemmas found in both texts that occur at most 3 times in the rest of the New Testament.
  Rate per 1,000 words of the shorter text.
- **Shared strings:** distinct sequences of 4 lemmas (all words) found in both texts. Rate per 1,000 words of the
  shorter text; the longest shared sequence is also reported.
- **Same order:** Spearman correlation between the positions (first occurrence, as a share of the text) of the
  rare shared words in the two texts. Only computed when there are at least 6.

**Known borrowing (the calibration pairs):** 2 Peter and Jude; Ephesians and Colossians; 2 and 1 Thessalonians.
Matthew and Mark, and Luke and Mark, are reported for reference, though no letter pair is as long.

**Controls:** every other pair of the 21 New Testament letters (Romans to Jude, Hebrews included). Excluded are
pairs with a claimed literary relationship: the calibration and test pairs, 1 Peter with 2 Peter, the three
Pastorals with each other, the three letters of John with each other, and Colossians with Philemon. Each pair under
test is compared with the controls whose shorter text is between half and twice as long as its own shorter text.

**Decision rule:** a pair counts as "borrowing-like" if it is above the 95th percentile of its comparable controls
on shared strings *and* above the 90th percentile on rare shared words. A pair above on rare shared words only
counts as "shared vocabulary or tradition". Order is reported but not used in the rule.

## 3. Measures for passages

**Mark 12:13-17 and Romans 13:1-7.** Content lemmas (nouns, verbs and adjectives, excluding εἰμί, λέγω and
γίνομαι). Similarity: the sum, over the distinct content lemmas the two passages share, of each lemma's
inverse document frequency (log of the number of New Testament verses divided by the number containing it).
- Compare Romans 13:1-7 with every window of 5 consecutive verses in Mark, and rank 12:13-17 among them.
- The same for every window of 7 verses in 1 Peter (1 Peter 2:13-17 is the usual parallel to Romans 13).
- Benchmark: Mark 12:13-17 against Matthew 22:15-22 and Luke 20:20-26 (known copying).
- Report shared strings of 3 or more words.

**The Last Supper (supper.py).** Passages:
- Mark 14:22-25; Matthew 26:26-29; Luke 22:15-20 (also 22:19-20 alone, and the "shorter text" 22:15-19a without
  19b-20, which Codex Bezae and some Old Latin manuscripts have);
- 1 Corinthians 11:23-26;
- Justin, First Apology 66.3; Didache 9-10.

Measure: plain word forms (accents removed), so that texts without lemmas can be compared. For each pair: shared
2-word and 3-word sequences, and the agreements found in exactly two of the four canonical accounts.

Marcion's gospel: Tertullian, Against Marcion 4.40 (Latin), is read for which form of the bread and cup words it
reports.

## 4. Predictions

Borrowing:
- **B1.** All three calibration pairs are "borrowing-like" under the rule. If not, the rule is too weak and its
  verdicts below are reported as such.
- **B2.** 1 Peter and Hebrews are *not* "borrowing-like". At most they are "shared vocabulary or tradition".
- **B3.** 1 Peter shares more strings with Romans and with Ephesians than with Hebrews.
- **B4.** Mark 12:13-17 is in the top 10% of Markan windows for similarity to Romans 13:1-7, because of the topic
  (paying what is owed to authorities). It shares no string of 3 or more words with Romans 13, unlike its parallels
  in Matthew and Luke.
- **B5.** 1 Peter 2:13-17 is the 1 Peter window most similar to Romans 13:1-7.

The Last Supper:
- **S1.** Matthew and Mark share more 3-word sequences than any other pair (the copying benchmark).
- **S2.** Luke 22:19-20 shares more 2- and 3-word sequences with 1 Corinthians 11:23-25 than with Mark 14:22-24.
- **S3.** Luke 22:15-18 shares more with Mark 14:25 than with 1 Corinthians.
- **S4 (description; read in advance).** Justin's quotation combines "do this in remembrance of me" (Luke/Paul)
  with "this is my blood" (Mark/Matthew), not "this cup is the new covenant in my blood".
- **S5.** Tertullian, Against Marcion 4.40, shows that Marcion's gospel had a cup saying with "covenant" in "my
  blood", the Luke/Paul form.
- **S6.** The Didache's eucharist prayers (9-10) share none of the institution words "body", "blood" and
  "remembrance" with 1 Corinthians 11. Not every eucharist liturgy of the period used Paul's wording.

**What the Supper test can decide:** whether Luke's bread and cup words are tied to Paul's more than to Mark's.
**What it cannot decide:** whether Luke copied Paul's letter or both used the same church liturgy, and which came
first. This is stated in advance so that a clear tie is not read as more.

## 5. Limits stated in advance

- Word-overlap measures detect shared wording, not direction. Direction needs qualitative criteria (which version
  fits its context better, which smooths the other), and these are not coded here.
- Shared quotations of the same scripture inflate overlap without either text borrowing from the other. The shared
  strings are listed so this can be checked by eye.
- The NT is small: "rare in the rest of the NT" is a crude measure of rarity. The LXX would be better.
- Coding rules are by Claude (an AI model).
