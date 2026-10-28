# A hidden hand, a writer of many voices, and Paul (attic_hands)

Pre-registered (PREDICTIONS.md, SHA-256 47f9e83a…adf). Results: RESULTS.md. Two fixes, both made before reading any
result as evidence, are in AMENDMENTS.md 1-2. Rules by Claude (an AI model), for review.

## Why the Attic orators

Livesey's model needs two things: writers who compose convincingly in someone else's voice, and a corpus under one
famous name that is really several hands. Our one-hand study could not tell whether stylometry sees either, because
single letters are too short. Classical Athens has known cases at the length of Paul's longer letters. These are
function-word tests: the small, unconscious words, which are hard to fake.

## B. A second hand inside a famous name: found, perfectly

Six speeches transmitted as Demosthenes' were in fact written by Apollodorus (46, 49, 50, 52, 53, 59). They were
mixed with Demosthenes' 12 genuine private speeches, all of them lawsuits, so genre gives nothing away. Then every
speech was ranked by how far it stands from the others, without telling the computer which was which.

**All six Apollodoran speeches came out on top, ranks 1-6** (AUC 1.00, against a chance level of 0.50). Every one
lies beyond the most distant genuine speech. Both predictions are met.

On the two disputed speeches, the method takes sides. Speech 47 ranks 3rd, with Apollodorus, which supports
MacDowell's attribution. Speech 45 ranks 13th of 20, with Demosthenes, which supports those who give it to
Demosthenes. With the public speeches added, which differ in genre, the Apollodoran speeches still score high
(AUC 0.81), though the big public orations (On the Crown, Against Timocrates) now join them at the top.

**What it means:** a second writer of ordinary skill, hidden inside a famous author's corpus, is visible at speech
length when the genre is held constant. The method can see a hidden hand. So when it does not, at that length and
in one genre, that is information.

## A. A writer behind many voices: recognisable, but not reliably

Lysias wrote courtroom speeches for clients to deliver as themselves: a betrayed husband, a disabled man, a farmer.
Each speech was attributed among eight orators of his time, with the speech itself left out of training.

| writer | passages to the right writer | speeches to the right writer |
|---|---|---|
| Lysias | 58% | 67% |
| Isaeus | 63% | 73% |
| Isocrates (forensic) | 67% | 67% |
| Apollodorus | 77% | 100% |
| Demosthenes (private) | 90% | 92% |
| Antiphon | 90% | 100% |
| Aeschines | 93% | 100% |

Chance is 12.5%. **Prediction A narrowly fails** (60% and 70% were required). Lysias, the master of character-writing,
is the hardest of the main writers to recognise: about six speeches in ten. Most of the misses are his shortest
speeches, which give only one or two passages. The famous "On the Murder of Eratosthenes", spoken by a betrayed
husband, goes to Andocides.

**What it means, honestly:** writing in other people's voices *does* blur a writer's hand, though far from
completely. This is a point for Livesey. A school writing in Paul's voice need not leave a clear trace of its own
writers.

## C. The same ranking on Paul: it picks out the core four, not the Pastorals

The identical unlabelled ranking on Paul's 13 letters put **the core four at the top** (1 Corinthians, Romans,
Galatians, 2 Corinthians) and the Pastorals at the bottom. Both predictions fail (Pastorals AUC 0.00).

This is not a sign that the core four are the odd ones out in authorship. The Demosthenes test was built to hold
genre constant, all private lawsuits. Paul's corpus is not like that. The core four are long arguments, and the
other nine are mostly short exhortations. "Far from the rest" therefore finds the minority style, which here is the
core four. In Paul's corpus, this ranking measures genre and length, not hands.

Exploratory (AMENDMENTS.md 3): measured instead as distance from the core four, the most distant letters are
Ephesians, 1 Timothy and 2 Timothy, then Philemon, Colossians and Titus. Inside the core four, 2 Corinthians stands
furthest from the other three, about as far as 2 Thessalonians. That is roughly the usual scholarly picture
(Ephesians and the Pastorals most doubted), but with labels assumed. The Pastorals' AUC against the other non-core
letters is 0.72.

## What this adds to the Livesey question

- **The method works when the comparison is fair.** It found Apollodorus inside Demosthenes perfectly. So the
  earlier failures (one_hand, Laodiceans) were about length and genre, not a method that can never see a second hand.
- **But one voice can mask a writer.** Lysias shows that deliberate character-writing makes a writer harder to
  recognise. A skilled school writing as Paul could blur its hands in the same way.
- **Paul's letters are the hard case.** Applied to Paul, the method is confounded by genre, and the disputed
  letters do not separate cleanly. Measured against the core four, the doubted letters (Ephesians, the Pastorals)
  are the ones that stand furthest away, as most scholars would expect. But nothing here proves the core four are
  one hand, or that they are not.

So the honest summary: stylometry can find a hidden hand inside a corpus of similar texts, and can be partly
defeated by writing in character. On Paul it neither confirms nor refutes a school.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| A. Lysias: at least 60% of passages and 70% of speeches attributed to him | narrowly not met: 58% and 67% (chance 12.5%) |
| B1. Apollodorus AUC at least 0.80 | met: 1.00 |
| B2. At least 4 of 6 Apollodoran speeches beyond every genuine speech | met: 6 of 6 |
| C1. Pastorals AUC at least 0.80 | not met: 0.00; the ranking picks out the core four (genre) |
| C2. No core letter among the four most distant | not met: the core four are ranks 1-4 |

## Running it

    python attic_hands/fetch_texts.py
    python -X utf8 attic_hands/attic_hands.py

## Sources for the attributions

- MacDowell, Demosthenes the Orator (2009), as reviewed at bmcr.brynmawr.edu/?p=27610 (Apollodorus: 45, 46, 47, 49,
  50, 52, 53, 59).
- Trevett, Apollodoros the Son of Pasion (1992).
