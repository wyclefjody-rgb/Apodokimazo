# Did Marcion's school write Paul's letters, or edit them?

Two pre-registered tests (PREDICTIONS.md, SHA-256 3c8dfa4b…c3c7, written before either was run). Coding by Claude
(an AI model), for review. Generated tables: BACKREFS.md (Part A) and TERTULLIAN.md (Part B).

## The question

Nina Livesey proposes that the letters were composed about 144 CE in Marcion's school, as a collection. Recent
Marcion scholars (Vinzent; Schmid, endorsed by Litwa) hold that Marcion edited letters that already existed. Two
things can be tested with the texts we have:
- **Part A.** Do the letters refer back to one another in a way that fits one collection order better than another?
  Vinzent reads Galatians 5:21 ("as I warned you before") as pointing back to 1 Corinthians, although Marcion put
  Galatians first. If that held, Marcion's order would be a rearrangement of an older collection.
- **Part B.** Did Marcion's own edition contain material that contradicts Marcion's theology? Tertullian's Against
  Marcion, Book 5, goes through that edition letter by letter. A school writing letters to carry Marcion's
  theology should not have written passages that refute it.

## Part A: back-references (BACKREFS.md)

The script finds 91 verses in the ten letters with a verb or noun of saying, writing, teaching or handing on in a
past sense. Coded by what they point back to:

| points to | verses |
|---|---|
| oral teaching or a warning given during a visit | 18 |
| an earlier passage of the same letter | 5 |
| an earlier letter to the same church | 11 |
| another letter of the collection | 1 |
| unclear | 7 |
| not a back-reference (scripture, "this letter", other senses) | 49 |

- **Galatians 5:21** is coded as oral. Paul's other uses of the same verb ("I told you before") say outright that
  the warning was given in person: "when we were with you, we told you beforehand" (1 Thessalonians 3:4; also 4:6
  and 2 Corinthians 13:2). The shared phrase with 1 Corinthians ("will not inherit the kingdom of God") is real, but
  the verb points to speech, not to a letter.
- **The one cross-letter reference**, Colossians 4:16 ("the letter from Laodicea"), points to Ephesians only if
  Ephesians is that letter, which was Marcion's own identification. Ephesians comes before Colossians in all three
  orders tested (Marcion's, the later canonical order, and P46), so it cannot tell them apart.

**Result:** Part A cannot decide, as predicted. The back-references are almost all to visits and to earlier
letters to the same church, which fits real correspondence and is no help in ordering a collection. Vinzent's
argument from Galatians 5:21 is weak.

## Part B: what stood in Marcion's own edition (TERTULLIAN.md)

Every passage of Paul that Tertullian quotes or discusses in Book 5 was coded (170 codes). Each code cites the
chapter and a few Latin words, which the script checks against the text.

| Tertullian says the passage was... | against Marcion on its face | against him only by Tertullian's argument | neutral or for Marcion |
|---|---|---|---|
| in Marcion's edition | 17 | 124 | 11 |
| removed, added to or altered by Marcion | 10 | 4 | 1 |
| unclear | 3 | 0 | 0 |

**The pre-registered rule** was that 10 or more passages both in Marcion's edition and against his theology on
their face count as clear evidence against Marcionite composition. The count is 17.

How robust that is depends on how much weight the weaker codes carry:

| counting | passages |
|---|---|
| every "on its face" code | 17 |
| strong and medium only | 12 |
| strong only | 5 |
| only those Tertullian *says* Marcion kept | 2 |

The five strong ones are the core of the result:
- **1 Corinthians 8:6:** "for us there is one God, the Father, from whom are all things".
- **1 Corinthians 9:9-10:** "it is written in the law of Moses, You shall not muzzle the ox ... it was written for
  our sake".
- **1 Corinthians 10:1-4:** "our fathers" in the wilderness drank from the spiritual rock, "and the rock was Christ".
  Tertullian says outright that Marcion kept this ("Etiam Marcion servat", 5.5) and "stumbled on the rock" (5.7).
- **1 Corinthians 10:6-11:** Israel's punishments "happened as examples for us" and "were written down for our
  instruction".
- **2 Corinthians 4:6:** "the God who said, Let light shine out of darkness, has shone in our hearts ... in the face
  of Christ". Tertullian says Marcion "did not see" this end of the sentence (5.11).

The medium ones are mostly citations of Israel's scriptures with "it is written" or "the law says" as authority
(1 Corinthians 1:19, 3:19-20, 14:21, 14:34, 15:54-55), plus "the law is holy, and the commandment holy, just and
good" (Romans 7:12) and the gentiles "without God" because "alienated from the commonwealth of Israel" (Ephesians
2:12). Eleven of the 17 are in 1 Corinthians; Galatians, the most anti-law letter, has none.

**What Tertullian says Marcion cut** runs the other way. Of the 15 changes he reports, 10 remove or alter wording
that would be "against on its face": Abraham as father of believers (Galatians 3:6-9), Christ as Abraham's
promised seed (3:16), a wide gap in Romans 8-11 (if it covered the whole span, it took out Christ "from Israel
according to the flesh", 9:5), "God who created all things" (Ephesians 3:9), "in him all things were created" (Colossians 1:16), "the last
Adam" (1 Corinthians 15:45), "the apostles and prophets" (Ephesians 2:20), "the first commandment with a promise"
(Ephesians 6:2).

## What this means

- **Against Marcionite composition.** By Tertullian's report, Marcion's own edition still said that the Father is
  the one "from whom are all things", that the God of the gospel is the God who said "Let light shine", that the
  wilderness rock was Christ, and that Israel's scriptures were "written for our sake". A school composing letters
  to carry Marcion's theology would not write these. Livesey's model needs either a school that wrote or kept
  material refuting its founder, or a Tertullian who misreports Marcion's text.
- **The pattern fits an editor.** What Marcion is said to have cut is the most explicit material (Abraham, Israel,
  the Creator of all things); what survived is mostly less obvious or embedded in argument. That is what one
  expects when an editor works over an existing text and misses things, which is how Tertullian himself frames it
  ("I take what he did not see to erase as his carelessness and blindness", 5.13).
- **But not the direction of the changes.** Vinzent and others argue that Marcion's text is the older one and the
  catholic text added material. The list of changes alone cannot settle who changed what, because Tertullian
  assumes his own text is the original. The 17 passages are different: they are in Marcion's text on any view of
  priority.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| 1. Most back-references point to visits or earlier letters to the same church | met: 29 of the 42 real back-references |
| 2. Galatians 5:21 refers to a warning given in person | met as coded |
| 3. Part A cannot decide | met: the one cross-letter reference fits every order |
| 4. Tertullian attributes 15 or more passages he uses against Marcion to Marcion's text | met: 141 |
| 5. At least 10 of them are against Marcion on their face | met: 17 (12 without the weak codes; 5 strong). Both named examples failed: Romans 1:3 is not in Book 5 and Galatians 4:4b is "unclear" (AMENDMENTS.md 3) |
| 6. Most of Tertullian's arguments are interpretive | met: 124 of 152 |
| 7. Reported deletions are mainly in Romans 9-11, Romans 15-16 and Galatians 3 | partly: Romans 9-11 and Galatians 3 yes; Romans 15-16 only implied; Ephesians has as many reported changes (5) as Galatians (4), and changes are reported in 7 of the 10 letters |

## Limits

- **Tertullian is the only witness used, and he is hostile.** For 15 of the 17 passages he argues from the text
  as Marcion's without saying in so many words that Marcion kept it. He may sometimes have quoted his own copy.
- **The strength line is a judgment.** The pre-registered rule counts all 17. A reader who accepts only the five
  strong passages, or who thinks a Marcionite could cite the Creator's scriptures for argument's sake, gets a count
  below 10. The result rests mainly on 1 Corinthians 8-10 and 2 Corinthians 4:6.
- **Old Latin text.** Oehler (1854). Modern editions (Kroymann, Evans) may differ in places that matter.
- **Coding is by an AI model** and every code needs a human check (tertullian_codes.txt has the Latin and the reason
  for each).

## Next checks

1. **Epiphanius.** His Panarion (42) lists Marcion's readings independently of Tertullian. Checking the 17 against
   that list would test the weakest link, Tertullian's reliability, directly.
2. **Modern reconstructions.** Compare the 17 with the reconstructions of Marcion's Apostolikon (Schmid 1995 and
   later work), passage by passage.
3. **Review the medium codes** (tertullian_codes.txt). Each one moved from medium to weak or "by argument" lowers the
   count by one; the strong five do not depend on them.

## Running it

From the kit folder:

    python -X utf8 marcion_text/backrefs.py
    python -X utf8 marcion_text/tertullian.py

tertullian.py clones only Against Marcion from Perseus's canonical-latinLit into the kit (canonical-latinLit/) the
first time, and writes the extracted Latin to marcion_text/adv_marc_5.txt. Keep both out of public uploads.
