# Which came first, Acts or Paul's letters? Predictions and rules

Written 2026-10-23, before any count below was run. Never edited; changes go in AMENDMENTS.md with a date.

## 1. The question

Most scholars hold that Paul's letters were written first (50s) and Acts later (c. 80-130); some (Pervo) argue Acts
used the letters. Nina Livesey argues the reverse: Acts came first and created the figure of Paul, and the letters
were written in his voice c. 144, partly correcting Acts (her interview series, Secular Frontier, 2025). The Paul map
(paul_map/) shows that the two tell the same outline and conflict at points, but it cannot say which way the
borrowing ran. This study tries to.

The idea is the one used on the gospels: when one writer borrows from another, the source's habits of language leak
into the borrower's text where it follows the source, and not elsewhere. Luke's use of Mark is the textbook case,
and is used here as the positive control.

## 2. Data

SBLGNT with MorphGNT lemmas (sblgnt/). All counts are of lemmas. Proper names (lemmas starting with a capital) are
left out of every word list, since they would only show shared topic.

Passages (SBLGNT verse ranges):
- **Acts, Paul's speeches (target):** Ac 13:16-41; 14:15-17; 17:22-31; 20:18-35; 22:1-21; 24:10-21; 26:2-23; 28:17-20;
  28:25-28.
- **Acts, all other speeches (comparison):** Ac 1:16-22; 2:14-40; 3:12-26; 4:8-12; 5:35-39; 7:2-53; 10:34-43; 11:4-17;
  15:7-11; 15:13-21; 19:25-27; 19:35-40; 24:2-8; 25:14-21; 25:24-27.
- **The letters' passages about Paul's own life, those that Acts parallels (target):** Ga 1:11-2:14; 2Co 11:22-33;
  1Th 2:1-3:6; Php 3:4-6; Ro 15:14-33; 1Co 15:8-10; 1Co 16:1-12.
- **The rest of the seven undisputed letters (comparison).**
- **Narrative passages in the letters that have nothing to do with Acts (genre control):** Ro 4:1-25; Ro 9:6-18;
  1Co 10:1-11; Ga 4:21-31.
- **Luke's blocks taken from Mark (positive-control target):** Lk 4:31-6:19; 8:4-9:50; 18:15-21:38.
- **Luke's blocks not from Mark (positive-control comparison):** Lk 1:5-2:52; 6:20-8:3; 9:51-18:14.

Reference corpus (books that are neither Luke-Acts nor Pauline): Mt, Mk, Jn, Heb, Jas, 1-2 Pe, 1-3 Jn, Jude, Rev.
For the Mark control the reference drops Mt and Mk (both depend on Mark) and Lk-Acts.

## 3. Part A: leakage of characteristic words (computed by acts_order.py)

A word is **characteristic** of a writer if it occurs at least 5 times in that writer's base text and its rate there
is at least 4 times its rate in the reference corpus (reference count plus 0.5, to avoid dividing by zero). The base
texts leave out the passages being tested, so no list is built from its own target:
- **Pauline words:** base = the seven letters minus their autobiographical target passages.
- **Lukan words:** base = Luke + Acts 1:1-8:40, 9:32-11:24, 12:1-24 (the parts of Acts without Paul).
- **Markan words:** base = Mark; reference = Jn, Heb, Jas, 1-2 Pe, 1-3 Jn, Jude, Rev.

Statistic: the share of a passage's words that are characteristic words. Significance: 10,000 random draws of
passages from the comparison text, matched to the target in number and length of pieces (targets are cut into
pieces of at most 300 words); one-sided p = share of draws at least as high as the target. Seed 0.

Tests:
- **C (positive control):** Markan words in Luke's Markan blocks vs his other blocks. The method works only if this
  is clearly positive (p < 0.01). If it is not, Part A is reported but no conclusion is drawn from it.
- **D1 (Acts knew Paul's language):** Pauline words in Paul's speeches in Acts vs the other speeches in Acts.
- **D2 (the letters knew Acts' language):** Lukan words in the letters' autobiographical passages vs the rest of
  the letters.
- **G (genre control for D2):** Lukan words in the letters' non-Acts narrative passages vs the rest of the letters.
  Lukan words are partly narrative words, so D2 counts as evidence only if it is significant (p < 0.05) **and** the
  autobiographical passages' share is also higher than the genre-control passages' share.
- Sensitivity (reported, not decisive): thresholds of 2 and 8 instead of 4.

Reading the outcomes:

| D1 | D2 | reading |
|---|---|---|
| yes | no | Acts' author knew Paul's way of speaking (from the letters or from Pauline tradition); no sign the letters knew Acts' language. Fits letters-first. |
| no | yes | The letters' life-story passages use Acts' language. Fits Livesey's Acts-first. |
| yes | yes | contact both ways, or a shared milieu; undecided |
| no | no | no literary contact detectable by this method; undecided |

## 4. Part A2: shared phrases found nowhere else

Lemma three-word sequences, containing at least one noun, verb or adjective, found in both texts and in no book of
the reference corpus. Counted for Acts with the seven letters, and for Luke with the seven letters (same author,
similar length, but Luke is not about Paul). Every Acts-letters phrase is listed for reading. This measures contact
or shared topic, not direction.

## 5. Part B: which telling answers the other (hand-coded, in CHECKLIST.md)

For each episode the letters and Acts both tell (paul_map/), the coder asks three questions:
1. **Rebuttal:** does one text deny or head off something that only the other text says?
2. **Puzzle explained:** does one text explain something that is odd or unexplained in the other?
3. **Shared wording:** do they share a distinctive wording for the same detail?
Each item is coded "letters answer Acts", "Acts answers the letters", or "neither", with a reason and a strength.
A denial counts as a rebuttal only if the thing denied is specific to the other text; a general denial ("I do not
lie") counts only if it matches a claim the other text makes.

## 6. Predictions

1. C: Markan words are clearly more common in Luke's Markan blocks (p < 0.01). The method works.
2. D1: Paul's speeches in Acts have more Pauline words than the other speeches, modestly (p < 0.05), mostly in the
   Antioch and Miletus speeches (justification by faith, "the gospel of the grace of God", working with his own hands).
3. D2: the letters' autobiographical passages do not have more Lukan words than the genre-control passages.
4. A2: Acts shares more exclusive phrases with the letters than Luke does, but few, and mostly of topic (the
   collection, the escape from Damascus, Jerusalem).
5. Part B: mixed. Some Acts passages look like smoothings of the letters (the Jerusalem visits, Timothy, the collection
   as "alms"); some letter passages could be read as answers to Acts (Galatians 1:17-24). No item is decisive.
6. Overall: the evidence leans letters-first, but does not exclude Livesey's order.

## 7. Limits stated in advance

- Leakage shows contact with a writer's language, not with a particular text: Acts' author could know Paul's idiom
  from his followers rather than his letters.
- The passages are short (Paul's speeches total about 2,000 words), so the tests have little power.
- Characteristic-word lists depend on the thresholds, which is why two others are reported.
- Part B is judgment and is open to the same review as the Daniel-method checklist.
