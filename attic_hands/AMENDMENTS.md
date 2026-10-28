# Amendments to PREDICTIONS.md (attic_hands)

PREDICTIONS.md is never edited (SHA-256 47f9e83a104f371aa1f348d9bf2091b5ffc771a67438e236267cb78ebcdd8adf).

## 1. 2026-10-27: Isocrates numbering (before the first run)

PREDICTIONS.md says "Isocrates 16-21 (his forensic speeches)", in the traditional numbering. Perseus numbers
Isocrates differently: its tlg016-tlg021 are Archidamus, On the Peace, Areopagiticus, Antidosis, To Philip and
Panathenaicus. The forensic speeches intended (traditional 16-21: Concerning the Team of Horses, Trapeziticus, Against
Callimachus, Aegineticus, Against Lochites, Against Euthynus) are Perseus tlg001-tlg006, and those are used.

## 2. 2026-10-27: the outlier distance was degenerate as first written

Section 3 says each text's profile is "compared with the profile of the rest of the corpus without it". Coded
literally, with z-scores taken over the whole corpus, the rest's average is always an exact negative multiple of the
text's own average. So every distance came out 2.000 (opposite directions), and the first run's rankings were
meaningless: all ties, ordered only by input. The distance is redefined as each text's **mean Cosine Delta distance
to every other text** of the corpus. That keeps the intent (how far a text stands from the rest, with no labels
used) and is the usual form. Everything else is unchanged. All results in RESULTS.md use the corrected distance.

## 3. 2026-10-27: exploratory, after seeing part C

The unlabelled ranking on Paul put the core four at the top and the Pastorals at the bottom (part C). In Paul's
corpus the core four are a minority style (argument) among mostly hortatory letters, so "far from the rest" picks
out the core four. Added, as exploratory only: each letter's mean distance to the core four. This uses labels (the
core four as "Paul"), so it is not part of any decision rule.
