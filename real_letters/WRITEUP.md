# Do genuine letters slip? The missing control for the slip test

Pre-registered (PREDICTIONS.md, SHA-256 4987661a…f143). Results: RESULTS.md. Every item and its evidence: codes.txt.
Decisions and the main weakness: AMENDMENTS.md 1-2. Coding by Claude (an AI model), for review.

## The question

slip_rate and third_corinthians showed that writings composed later in an earlier figure's name slip in about a
third of their checkable details. Paul's four main letters have none in 16. But that is only half an argument. Real
writers make mistakes too: a wrong date, a garbled name, a detail other evidence contradicts. If genuine letters
"slip" just as often under the same coding, Paul's clean record means nothing. This study measures it.

## What was done

Three collections of genuine Latin letters, dated and attributed by outside evidence, were read in full. Every
detail that can be checked against an independent source (historians, inscriptions, papyri, coins, law books, the
official lists of consuls) was coded with slip_rate's rule:
- **Pliny to Trajan** (c. 98-112): letters 1-60 and the two on the Christians, 96-97;
- **Cicero to Atticus**, Book 1 (68-61 BCE);
- **Seneca's Moral Letters** 1-30 (c. 63-65), literary letters closer to Paul's kind.

## Results

| | checkable details | slips | slip rate |
|---|---|---|---|
| Pliny | 25 | 0 | 0% |
| Cicero | 22 | 0 | 0% |
| Seneca | 12 | 0 | 0% |
| **all genuine letters** | **59** | **0** | **0%** (95% interval 0-6%) |
| **known later writings** (Pastorals, spurious Ignatius, Clementine letters, 3 Corinthians) | **51** | **18** | **35%** (24-49%) |

The two intervals do not come near each other. Genuine letters check out against outside evidence:
- Pliny reaches Bithynia on 17 September, in time for Trajan's birthday on the 18th.
- Cicero's candidates for the consulship match Asconius' list.
- Seneca's Atticus is correctly the grandfather-in-law of Tiberius.

The later writings fail on a third of their details.

**Paul's record weighed both ways.** A writer who checks out like the genuine letter-writers would come through
Paul's 16 details with no slip about 79% of the time. A writer like the known later writers would do so about 0.2%
of the time. So Paul's clean record is about **350 times more likely if the letters are genuine** than if they
were written later. Against all the later writings we have, including the careful Acts of Thomas, the ratio is
about 120 to 1. Against those closest in time to their setting, it is about 80 to 1.

All four predictions were met. As expected, Seneca has far fewer checkable details per 1,000 words (0.6) than Pliny
(4.6) or Cicero (2.4). Literary letters say less about the world.

## What it means

- **The slip test now has a measured false-alarm rate.** Under the same coding, genuine letters did not slip once
  in 59 checkable details. So a clean record is what genuine letters look like, and a third of details slipping is
  what later writing looks like. This is the step that turns the slip argument into a tested method.
- **For Paul,** the evidence of his four main letters favours genuine letters over later composition by a factor of
  roughly 80 to 350, depending on which later writings are used for comparison. That is strong evidence, not proof:
  how strongly to believe it still depends on everything else (the Acts of Thomas shows a later writer can be clean).
- **For the book,** this is the result of Chapter 6. It answers the obvious objection to Chapter 2 before a
  reviewer raises it.

## Limits

- **The coder knew which letters were genuine.** This is the main weakness. A blind recoding, by you or a second
  reader, with authors' names hidden, is the proper check (AMENDMENTS.md 2).
- **Latin letters of educated Romans,** not Greek letters of a Jewish teacher. This tests the method, not genre.
- **Circularity:** much of what we know about Cicero's and Pliny's times comes from these letters. Only details
  checkable elsewhere were counted, so many details were left out ("not").
- **Small numbers:** 59 genuine details. Zero slips is consistent with a true rate of up to about 6%.
- The citations in codes.txt were checked from memory against standard sources; each needs a look before
  publication.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| 1. Each collection's slip rate below 5% | met: 0% in all three |
| 2. Pooled genuine rate below 5%, intervals not overlapping the later writings' | met: 0-6% against 24-49% |
| 3. Likelihood ratio for Paul's record above 20 | met: 347 to 1 |
| 4. Seneca has fewer checkable details per 1,000 words | met: 0.6 against 4.6 and 2.4 |

## Running it

    python real_letters/fetch_texts.py
    python -X utf8 real_letters/real_letters.py

It reads slip_rate/codes.txt and third_corinthians/codes.txt, so both folders must be in the kit.
