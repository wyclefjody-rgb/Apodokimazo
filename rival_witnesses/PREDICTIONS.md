# Paul outside Marcion's circle, to about 160: predictions and rules

Written 2026-10-27, before rival_witnesses.py was written or run and before the witness texts were read for this
study. Never edited; changes go in AMENDMENTS.md with a date.

## 1. The question

Livesey dates the letters to about 144 and places them in Marcion's school. If so, by about 160 they would be at
most some 15 years old and would have come out of one Roman group. So:
- Did groups outside Marcion's circle (Valentinians, Basilides and his followers, Justin's circle, the circle of
  the Epistle of the Apostles) use Paul's letters by about 160?
- Did their Paul include passages that Marcion's edition lacked?

A fuller Paul in the hands of Marcion's rivals soon after 144 is hard to fit with letters that had just come out of
his school.

## 2. Declared in advance

From the literature, before reading the texts for this study, I expect:
- Ptolemy's Letter to Flora names "the apostle Paul" and quotes Romans 7:12, 1 Corinthians 5:7 and Ephesians 2:15.
- Justin never names Paul. Dialogue 27 has a chain of scripture verses in the order of Romans 3:10-18, and
  Dialogue 39 cites Elijah's complaint in a form close to Romans 11:3-4 (class B). Whether Justin knew Romans is
  debated.
- Origen (in Latin) reports Basilides on Romans 7:9. Hippolytus has Basilides' followers quoting Romans 8:19-22
  (class B) and 1 Corinthians 2:13.
- The Epistle of the Apostles has Jesus foretell Paul's conversion (chapters 31-33).
- The Treatise on the Resurrection cites "the apostle"; the Gospel of Truth echoes Colossians 2:14.

## 3. Witnesses

**Tier 1: non-Marcionite, usually dated before about 160, and preserved in their own words** (not paraphrased by an
opponent):

| witness | group | usual date | language | preserved in |
|---|---|---|---|---|
| Basilides, fragments by name | Basilidian | c. 117-138 | Greek | Clement of Alexandria, Stromata |
| Valentinus, fragments | Valentinian | c. 136-160 | Greek | Clement, Stromata |
| Ptolemy, Letter to Flora | Valentinian | c. 150-160 | Greek | Epiphanius, Panarion 33.3-7 |
| Justin, 1 Apology and Dialogue | Justin's circle (anti-Marcionite) | c. 150-160 | Greek | direct |
| Epistle of the Apostles | anti-Gnostic | c. 140-170 | Ethiopic, Coptic | direct (translation) |

**Tier 2: later, or reported by others**, reported separately:
- the Basilidians in Hippolytus, Refutation 7.20-27 (Greek; Hippolytus c. 225; his source undated);
- Theodotus, in Clement's Excerpts from Theodotus (Greek; c. 160-170, preserved c. 200);
- the Valentinian Nag Hammadi texts: Treatise on the Resurrection, Gospel of Truth, Prayer of the Apostle Paul
  (Coptic; 2nd century, dates disputed);
- Basilides on Romans 7:9 in Origen's Commentary on Romans (Latin translation by Rufinus).

Dates are the usual ranges in standard reference works and need checking. Livesey re-dates 1 Clement, Ignatius and
Polycarp to 140-150; she is not known to re-date these witnesses.

## 4. Coding

Each use of a letter of Paul is coded with:
- witness, place, Pauline passage(s);
- **grade:**
  - **Q**: named as Paul's or "the apostle's", with recognisable wording;
  - **V**: verbatim, at least four consecutive words in Paul's order (after the kit's normalisation), not found
    in that form in the LXX;
  - **A**: allusion: distinctive wording or idea tied to one passage, but fewer shared words;
  - **D**: doubtful: could come from the LXX, a common phrase, or another source.
- **Marcion class** of the passage, as in early_witnesses/ALLUSIONS_PREDICTIONS.md: A in Marcion's edition, B
  absent, C probably absent (Romans 15-16), D the Pastorals; changed phrases count as B only if the witness has the
  words Marcion's text lacked.

**How candidates are found.**
- Greek witnesses: rival_witnesses.py lists every 4-word sequence shared with Paul's 13 letters and absent from the
  LXX, plus every mention of Paul or "the apostle". Every candidate is then read and coded by hand, with a reason.
- Non-Greek witnesses: the scripture references in a published translation, each checked against Paul's text and
  coded by hand. Translation means verbatim cannot be judged, so the best possible grade is A, or Q if Paul or
  "the apostle" is named.

## 5. Predictions

1. At least 3 of the 5 tier-1 witnesses have at least one use graded Q or V.
2. Ptolemy names Paul or "the apostle" and quotes at least two different letters.
3. At least one tier-1 witness has a use graded Q, V or A of a class B, C or D passage.
4. Tier 2 has at least 3 uses graded Q or V of class B, C or D passages.
5. Justin never names Paul.

## 6. Decision rules

- **Q or V use of a class B or C passage by a tier-1 witness:** a Paul fuller than Marcion's edition was in the
  hands of his rivals by about 160. On Livesey's dating that means within some 15 years of composition, across rival
  groups. Counted as good evidence against her model. Grade A alone counts as a hint.
- **Tier-1 uses only of class A passages:** consistent with Marcion's edition being the Paul that spread. Counted as
  a point for her model.
- **Tier-1 uses of class D (the Pastorals):** the additions Marcion's collection lacked were in circulation;
  reported, but not decisive, since the Pastorals could date to the 140s.
- **Named use (Q) by non-Marcionite groups:** shows Paul's authority across rival groups by about 160. That bears on
  where his authority came from, not directly on the date of the letters.

## 7. Limits stated in advance

- Few tier-1 texts survive, and most are short (fragments; Ptolemy's letter about 2,000 words).
- Fragments survive because later writers chose to quote them, often for their use of scripture.
- Justin's possible use of Romans can come through a shared collection of proof texts. The LXX filter and the
  grades are meant to catch this, not to settle it.
- Coptic and Ethiopic texts are coded from translations.
- Coding by Claude (an AI model), for review.
