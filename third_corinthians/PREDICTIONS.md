# 3 Corinthians and the Latin forgeries of Paul: predictions and rules

Written 2026-10-27, before the text was extracted, read or coded, and before third_corinthians.py was written. Never
edited; changes go in AMENDMENTS.md with a date.

## 1. Why

3 Corinthians is a known forgery in Paul's name, from the 2nd century. It is an exchange: a letter from the
Corinthians to Paul, and Paul's reply. Its lateness is known from outside evidence, not from its own slips:
- Tertullian (On Baptism 17, c. 200) says the Acts of Paul, which contain it, were written by a presbyter of Asia
  who was removed from office for it.
- It is absent from Marcion's collection and from the early Greek lists of Paul's letters.
- Its oldest copy, Papyrus Bodmer X, is from the 3rd century.

So it can serve two earlier studies:
- **Part A: slip_rate.** It is the closest-in-time control with an outside date that slip_rate could not code
  (slip_rate/WRITEUP.md, Limits).
- **Part B: rhetoric_across.** It is a second forgery of Paul surviving in Latin, much longer than Laodiceans.

Text: Léon Vouaux, Les Actes de Paul et ses lettres apocryphes (Paris, 1913), from the user's scan. Vouaux prints a
critical Latin text with a French translation. If the scan also has the Latin letters of Paul and Seneca, Paul's
side of them is added to Part B as a third Latin forgery.

## 2. Declared in advance

From the literature, I know the outline of 3 Corinthians:
- the Corinthians report two teachers, Simon and Cleobius;
- these teachers deny the resurrection of the flesh, that God made the world and man, that the Lord came in the
  flesh and was born of Mary, and the authority of the prophets;
- Paul's reply, written from prison in Philippi, answers point by point (the seed, Jonah, the bones of Elisha).

I know the Paul and Seneca letters are a 4th-century Latin forgery in literary Latin.

## 3. Part A: slips

**Method.** The whole text (both letters, and any framing narrative printed with them) is read in Latin and French.
Every datable item is coded with slip_rate's categories and codes (slip_rate/PREDICTIONS.md section 3):
- categories: church offices; the name "Christian"; Jerusalem and the Temple; circumcision and the synagogue;
  persons with known dates; written texts and scripture; heresies; rulers; persecution; the expected end;
- codes: fits (fits the setting, the 50s), slip (fits only a later time, or gets the setting wrong), either, not
  datable;
- slips are graded strong, medium or weak, with a reason.

The text is short, so it is read in full instead of searched by terms. This is a difference from slip_rate, stated
here.

**Predictions:**
- **A1.** 3 Corinthians has at least one slip.
- **A2.** Its slip rate is between 15% and 50%, like slip_rate's Group A (33% pooled).
- **A3.** Added to Group A as a sensitivity check, the probability of Paul's clean record (0 slips in 16 items)
  stays below 0.05.

**Rule.** If A1 fails (a forgery with an outside date and no slips), that is a second Acts of Thomas: evidence that
careful later writers can avoid slips, and a point for Livesey's escape route. It would be reported as such.

## 4. Part B: Latin style

**Method.** rhetoric_across's Part 2 measures, unchanged:
- **L1:** the share of the text's 3-word sequences found in the Latin Paul (Clementine Vulgate), against passages of
  Paul of the same length compared with his other letters;
- **L2:** the argument score per 1,000 words, against passages of Paul of the same length.

The forger's Latin is an older translation, not the Vulgate, so L1 undercounts borrowing, as it did for Laodiceans.

**Predictions:**
- **B1.** 3 Corinthians shares more 3-word sequences with Paul than the median passage of Paul does (imitation),
  but not more than every passage.
- **B2.** 3 Corinthians' argument score is within Paul's range (above his 5th percentile). It argues (the seed,
  Jonah, Elisha), so it should not look argument-free.
- **B3.** Paul's side of the Paul and Seneca letters, if in the scan, has an L1 share below the median passage of
  Paul and an argument score below Paul's 5th percentile. It is in polished literary Latin and does not imitate
  Paul's letters.

**Rule.** If B1-B2 hold and B3 holds, the style measures separate a forger who did not imitate Paul from Paul, but
not one who did. That is the lesson of one_hand and rhetoric_across, now at four times the length of Laodiceans.

## 5. Limits stated in advance

- OCR of a 1913 printing; every word list is checked by eye against the page images before use.
- A critical Latin text built from several manuscripts is not one ancient copy.
- 3 Corinthians may have existed before the Acts of Paul and been taken into it; its date is uncertain within the
  2nd century (usually c. 150-190).
- Coding by Claude (an AI model), for review.
