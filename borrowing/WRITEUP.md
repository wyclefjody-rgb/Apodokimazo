# Who borrowed from whom? (borrowing, with the Last Supper test)

Pre-registered (PREDICTIONS.md, SHA-256 35906bca…198e). Generated tables: BORROWING.md and SUPPER.md. Rules by
Claude (an AI model), for review.

## How borrowing is detected here

Three automatic measures on the Greek (MorphGNT lemmas):
1. **rare shared words:** words in both texts that are rare in the rest of the New Testament;
2. **shared strings:** identical 4-word sequences;
3. **order:** whether the shared rare words come in the same sequence.

Before testing a claim, the measures were tried on pairs where borrowing is known. Each pair was compared with
the 196 other pairs of New Testament letters, matched for length.

## 1. Calibration: the measures are only half reliable

| known borrowing | rare shared words (percentile) | shared strings (percentile) | same order | passes the rule? |
|---|---|---|---|---|
| Ephesians / Colossians | 100 | 100 | 0.87 | yes |
| 2 Peter / Jude | 99 | 80 | 0.98 | no (strings) |
| 2 / 1 Thessalonians | 88 | 100 | 0.36 | no (rare words) |

Borrowing comes in two styles. Ephesians reuses Colossians's *sentences* (a shared string of 19 words). 2 Peter
reuses Jude's *ideas and rare words* in its own sentences, with the same order (0.98). So the pre-registered rule,
which needed both measures, missed two of three known cases. Its "no" therefore clears nobody (AMENDMENTS.md 2).
A "yes" or a high score on either measure still means something.

## 2. 1 Peter and Hebrews (Carrier, citing Meyers)

| pair | rare shared words (percentile) | shared strings (percentile) | same order |
|---|---|---|---|
| 1 Peter / Hebrews | 91 | 34 | -0.47 |
| 1 Peter / Romans | 98 | 84 | -0.13 |
| 1 Peter / Ephesians | 59 | 76 | 0.45 |
| *2 Peter / Jude (known)* | *99* | *80* | *0.98* |

- **The rare words 1 Peter shares with Hebrews are telling:** Sarah, milk, the ark, "sojourners", "sprinkling",
  "antitype", "oracles", "fellow heirs", "undefiled". Few other pairs of letters of this size share as many (91st
  percentile). The link is real.
- **But it has none of the copying signs.** Hebrews and 1 Peter share almost no wording (34th percentile, an
  ordinary level). The longest shared string is a set phrase, "for ever and ever". The shared ideas run in
  *opposite* order (-0.47). Compare 2 Peter and Jude, which keep their source's order almost perfectly.
- **1 Peter is closer to Romans than to Hebrews** on both counts. The two letters even join the same two Isaiah
  verses into one "stone" quotation ("Behold, I lay in Zion a stone of stumbling and a rock of offence"). That
  famous combination is the most distinctive single contact between 1 Peter and any of the three letters.

**Verdict:** this fits shared vocabulary and tradition (common sermon images such as Noah's ark, sprinkled blood
and sojourners), or at most a loose knowledge of one text by the other. It does not fit the copying seen in the
known cases. That matches Carrier's own "pretty convincing… not a slam dunk". Direction cannot be measured this
way; it needs Meyers's kind of qualitative case.

## 3. Mark 12 "render to Caesar" and Romans 13 (Carrier: Mark puts Paul's teaching into Jesus' mouth)

- Against Romans 13:1-7, Mark 12:13-17 ranks **214th of 669** five-verse windows of Mark. A third of Mark is closer
  in vocabulary. They share only "God" and "give back", and no wording.
- **Luke's version is the one closest to Romans 13:** it changes Mark's Latin loanword κῆνσος ("census tax") to
  φόρος ("tribute"), Paul's word in Romans 13:6-7, and adds ἐξουσία ("authority"). So if any gospel echoes Romans
  13's vocabulary, it is Luke, not Mark.
- 1 Peter 2:13-19 is the window of 1 Peter closest to Romans 13 (rank 1 of 99): "be subject", "governing",
  "praise", "fear", "conscience". That fits the usual view that 1 Peter knows Romans.

**Verdict:** wording gives no support to Mark drawing on Romans 13. Carrier's argument is about theme (a scene
invented to carry Paul's teaching), and a word count cannot rule that out. But a theme alone is weak evidence of
borrowing: the saying's point (pay Caesar, but give God his due) is not Paul's point (authorities are God's
servants).

## 4. The Last Supper

| comparison | shared 3-word sequences |
|---|---|
| Mark / Matthew (known copying) | 27 |
| Luke 22:19-20 / 1 Corinthians 11:23-25 | 16 |
| Luke 22:19-20 / Mark 14:22-24 | 5 |
| Luke 22:15-18 / Mark 14:25 | 7 |
| Luke 22:15-18 / 1 Corinthians | 0 |

- **Luke's bread and cup words come from the same source as Paul's**, not from Mark: "do this in remembrance of
  me", "which is given for you", "after supper", "this cup is the new covenant in my blood". Twenty two-word
  sequences are found only in Luke and Paul. Luke's Passover saying before it (22:15-18) follows Mark instead.
- **The whole tie sits in 22:19b-20,** the verses missing from Codex Bezae and some Old Latin manuscripts. Luke's
  "shorter text" lines up with Mark (6 shared sequences) and hardly with Paul (2). Most editors accept the longer
  text. If it were a scribe's addition from 1 Corinthians, Luke would have no tie to Paul here at all.
- **Marcion's gospel had the longer text.** Tertullian (Against Marcion 4.40) starts from Luke 22:15 and reports a
  cup "establishing the covenant sealed in his blood" after the bread. That is the earliest evidence for 22:20
  (AMENDMENTS.md 3).
- **Justin (c. 150) mixes the two forms:** "do this in remembrance of me" (Luke/Paul) with "this is my blood"
  (Mark/Matthew). That looks like church practice blending the versions.
- **The Didache's eucharist prayers share none of the institution words** ("body", "blood", "remembrance",
  "covenant") and no 3-word sequence with any account. Not every church of the period used Paul's words.

**What this decides:** Luke's institution words and Paul's are tied, through a shared liturgical form or Luke's
knowledge of 1 Corinthians. **What it cannot decide:** which of the two it was, or what came first. For Livesey,
the tie fits her model as well as the standard one, because Marcion's own gospel carried the same wording.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| B1. All three calibration pairs pass the rule | not met: 1 of 3 (AMENDMENTS.md 2) |
| B2. 1 Peter / Hebrews not borrowing-like | met, but the rule's "no" is weak; the rare-word link is real |
| B3. 1 Peter shares more strings with Romans and Ephesians than with Hebrews | met (14.3 and 10.7 against 4.8 per 1,000) |
| B4. Mark 12:13-17 in the top 10% of Markan windows for Romans 13, with no shared strings | half met: no shared strings, but rank 214 of 669 (top 32%) |
| B5. 1 Peter 2:13-17 the closest 1 Peter window | met (rank 1 of 99) |
| S1. Mark / Matthew share the most | met (27) |
| S2. Luke 22:19-20 closer to Paul than to Mark | met (16 against 5) |
| S3. Luke 22:15-18 closer to Mark than to Paul | met (7 against 0) |
| S4. Justin mixes the two forms (read in advance) | as described |
| S5. Marcion's gospel had the Luke/Paul cup saying | met, on Tertullian's paraphrase (AMENDMENTS.md 3) |
| S6. The Didache shares none of the institution words | met |

## Limits

- Word overlap shows a relationship, never its direction.
- "Rare" means rare within the New Testament only; the Septuagint would give a better baseline.
- Shared quotations of scripture count as overlap. The Isaiah "stone" in 1 Peter and Romans may come from a common
  collection of proof texts, not from one letter.
- The calibration shows the rule misses paraphrase. A better version would weight rare words and order more and
  drop letter formulas (AMENDMENTS.md 2).

## Running it

From the kit folder, once:

    python borrowing/fetch_texts.py

then:

    python -X utf8 borrowing/borrowing.py
    python -X utf8 borrowing/supper.py
