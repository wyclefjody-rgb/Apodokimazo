# Do Paul's letters fit ancient letters, and does the misfit point to fiction? Predictions and rules

Written 2026-10-24, before letter_form.py was written or run. Never edited; changes go in AMENDMENTS.md with a date.

## 1. The question

Livesey (Westar interview, about 13:00-14:50) says that the 20th-century comparisons of Paul's letters with
everyday Greek papyrus letters "proved the reverse" of what they wanted. Paul's letters did not compare favourably,
and scholars explained this away by saying Paul adapted the form for his mission. She places the letters instead
among Roman literary letters.

Two questions:
1. **Is the misfit real?** How do Paul's letters compare with papyrus letters in length and in the standard
   formulas?
2. **Is the misfit a sign of fiction?** Writers who invented letters in someone else's name are the right test.
   They are the Greek fictional collections (Chion, Themistocles, the Cynic and Socratic letters and others) and
   the Christian forgeries (the Pastorals if not Paul's, the spurious letters of Ignatius). If invented letters
   depart from papyrus form the way Paul does, the misfit fits fiction. If they keep the everyday frame, or if
   Paul's departures are shared by Christian letters whatever their authenticity, the misfit is not a sign of
   fiction.

## 2. Data

Each letter is one unit.
- **Papyri:** the letter-period study's papyrus letters dated within 1-200 CE (letter_period/papyri_letters_accented.json).
  Papyri are often damaged, so lengths are also reported for "complete" papyri: an opening greeting in the first
  30 words and a farewell in the last 30.
- **Paul:** the thirteen letters, in four groups: core four, other undisputed (Php, 1Th, Phm), disputed (Eph, Col,
  2Th), Pastorals (1Ti, 2Ti, Tit).
- **Other New Testament letters:** Heb, Jas, 1Pe, 2Pe, 1Jn, 2Jn, 3Jn, Jude.
- **Early Christian letters:** Ignatius's seven (middle recension); spurious Ignatius (the same six letters as
  slip_rate); 1 Clement; Polycarp to the Philippians.
- **Greek literary letters:** Dionysius of Halicarnassus to Ammaeus and to Pompeius, Plutarch's Consolation to his
  wife, Arrian's Periplus.
- **Greek fictional letters:** Anacharsis, Chion, Phalaris, Themistocles, Crates, Socrates, the Socratics,
  Diogenes, Euripides, Brutus (from Hercher, via First1KGreek), Alciphron, Aelian, Philostratus.
- **Latin, for reference:** Cicero's letters to his friends and to Atticus (real correspondence); Seneca's moral
  letters and Pliny's letters (books 1-9; literary collections); Pliny book 10 (official correspondence with
  Trajan). Latin word counts run lower than Greek for the same content, so Latin lengths are compared within Latin
  only; Latin formulas are counted with their Latin equivalents.

Headings are kept: in the editions of the fictional collections the greeting ("Chion to Matris, greetings") is
printed as a heading, while in Paul and the papyri it is part of the text.

## 3. Measures

Words are counted after the kit's usual cleaning (lower case, no accents, Greek letters only; for Latin, letters
only).

| measure | Greek | Latin |
|---|---|---|
| length | words | words |
| everyday greeting | χαίρειν in the first 30 words | salutem, sal., s. or s. d. in the first 12 words |
| grace-and-peace greeting | χάρις and εἰρήνη both in the first 60 words | (none expected) |
| thanksgiving or blessing near the start | a form of εὐχαριστ- or εὐλογητός in the first quarter or the first 40 words, whichever is more | gratias ag- in the first quarter |
| everyday farewell | ἔρρωσο, ἔρρωσθε, ἐρρῶσθαι, ὑγίαινε, εὐτύχει or εὐτυχεῖτε in the last 30 words | vale or valete in the last 15 words |
| grace benediction at the close | χάρις in the last 40 words | (none expected) |
| greetings passed on | a form of ἀσπάζομαι in the last 30% of the letter | salut- in the last 30% |

**Profile distance.** For each group: the share of its letters with each of the five Greek formulas, and log10 of
its median length. The distance between two groups is the Euclidean distance between these six numbers. Greek
groups only.

## 4. Decision rules

- **Question 1** is answered "the misfit is real" if every letter of Paul is longer than the 95th percentile of
  complete papyrus letters, and fewer than 2% of papyrus letters have the grace-and-peace greeting or the grace
  benediction.
- **Question 2:** the Greek fictional letters as a whole are compared with Paul (all thirteen) and with the papyri.
  - If they are closer to Paul than to the papyri, the misfit fits invented letters (for Livesey).
  - If they are closer to the papyri, invented letters keep the everyday frame and the misfit is not a sign of
    fiction.
  - Separately, if the Pastorals and the spurious Ignatius letters are closer to Paul's core four than to the
    papyri, form cannot tell an authentic Christian letter from an imitation, in either direction.

## 5. Predictions

1. Every one of Paul's thirteen letters is longer than the 95th percentile of complete papyrus letters. Philemon is
   the shortest and the closest to the papyri.
2. Fewer than 1% of papyrus letters have Paul's grace-and-peace greeting or grace benediction.
3. Paul's median letter is longer than the median Greek fictional letter and the median Latin literary letter
   (Seneca, Pliny), and within a factor of two of the median letter of Ignatius.
4. The Greek fictional letters are closer to the papyri than to Paul: they keep the everyday frame (greeting and
   farewell) far more often than Paul, who never uses χαίρειν in a greeting or the everyday farewell.
5. The Pastorals and the spurious Ignatius letters are closer to Paul's core four than to the papyri.
6. Ignatius (genuine) mixes the two: an everyday greeting (χαίρειν) together with Pauline grace language.
7. Seneca ends nearly all his letters with "vale" (at least 90%), so in frame he is closer to everyday letters
   than Paul is.

Overall prediction: the misfit is real (Livesey is right about that), but it is a feature of early Christian
letters, real or imitated, not a mark of invented letters as such. On form alone the test cannot date Paul.

## 6. Limits stated in advance

- Formula detection by word lists is crude. A χάρις in the last 40 words can be an ordinary "thanks", and a
  heading can be an editor's.
- The fictional collections' greetings depend on how each edition prints headings.
- Papyrus lengths are lower bounds where text is lost.
- Most of the comparison material is Greek. The Latin is a reference only.
- Coding rules are by Claude (an AI model); the measures are automatic and listed in full in RESULTS.md.
