# Do genuine letters "slip"? Controls for the slip test: predictions and rules

Written 2026-10-27, before the texts were fetched, read or coded, and before real_letters.py was written. Never
edited; changes go in AMENDMENTS.md with a date.

## 1. Why

slip_rate and third_corinthians found that later writers in an earlier figure's name slip in about a third of their
datable items, while Paul's four main letters have none in 16. But a test is only as good as its error rate on
genuine cases. Real writers also make mistakes: a wrong date, a garbled name, a detail later evidence contradicts.
If genuine letters "slip" often under the same coding, Paul's clean record means little. If they almost never do,
the test separates real from later writing, and Paul's record can be weighed both ways.

## 2. Texts

Genuine letters whose date and author are known from outside evidence, with many checkable details, from Perseus
canonical-latinLit (Latin; slips are about content, not language):

| collection | sample | written | why |
|---|---|---|---|
| Pliny the Younger, Letters, Book 10 (with Trajan) | letters 1-60 and 96-97 | c. 98-112 | official correspondence: offices, rulers, places, laws; 96-97 are the letters on the Christians |
| Cicero, Letters to Atticus, Book 1 | all letters | 68-61 BCE | private letters full of named people, elections, trials, prices |
| Seneca, Moral Letters | letters 1-30 | c. 63-65 | literary letters to a friend, closer to Paul's genre; few datable items expected |

The sample is fixed here and not changed after reading.

## 3. What is counted

slip_rate's rule (slip_rate/PREDICTIONS.md section 3), with the setting = the letter's known date of writing:
- **datable item:** a person, office, place, event, institution, practice, text, price or expectation that can be
  checked against evidence independent of the letter;
- **fits:** fits that date and would be odd later; **either:** fits that date and later times too;
- **slip:** fits only a later time, or is wrong about the writer's own time or recent past as independent evidence
  shows (a genuine writer's error counts as a slip here: that is the false alarm being measured);
- **not:** not datable.

Items about the same fact in one letter are one item. Every letter in the sample is read in full, as 3 Corinthians
was; slip_rate's other controls were found by a term search. Each code gives its evidence. Coded by Claude (an AI
model), for review.

**Circularity.** Much of what we know about Cicero's and Pliny's times comes from these letters. A detail known only
from the letter itself cannot be checked and is coded "not". Only details checkable against other sources
(historians, inscriptions, coins, other writers, laws) count.

## 4. Predictions

1. **Each collection's slip rate is below 5%.**
2. **Pooled genuine rate below 5%,** and its 95% interval does not overlap the 95% interval of the pooled forgery
   rate (slip_rate Group A plus 3 Corinthians, 18 of 51).
3. **Likelihood ratio.** For Paul's record (0 slips in 16 items), the probability under the genuine letters' rate
   divided by the probability under the forgeries' rate (both Beta-binomial, as in slip_rate) is above 20.
4. **Seneca** has fewer datable items per 1,000 words than Pliny and Cicero (literary letters carry fewer checkable
   details).

## 5. Decision rules

- If 1-3 hold: the slip test separates genuine letters from later writing, with a known false-alarm rate. Paul's
  clean record then favours genuine letters by the likelihood ratio found. That is the validated version of the
  slip argument.
- If genuine letters slip at 10% or more: the test confuses ordinary error with lateness, and the slip argument
  weakens accordingly; the ratio is reported either way.
- Between 5% and 10%: reported as a weaker separation.

## 5. Limits stated in advance

- Three Latin collections by educated Romans, not Greek letters of a Jewish teacher. The test is of the method,
  not of genre.
- Reading in full finds more items than a term search; the item count differs from slip_rate's controls, though
  the rate is per item.
- Only errors that independent evidence can expose are counted, for genuine letters and forgeries alike.
- Coding by an AI model; every item has its reason, for review.
