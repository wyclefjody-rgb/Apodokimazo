# Can stylometry see a hidden hand, or a writer behind many voices? Attic orators as a test. Predictions and rules

Written 2026-10-27, before attic_hands.py was written or run. Never edited; changes go in AMENDMENTS.md with a date.

## 1. Why

Livesey's model needs writers who compose convincingly in someone else's voice (Paul's), and a corpus under one
famous name that is really the work of more than one hand. Our one-hand study could not test whether stylometry
sees such things, because single letters are too short. Classical Athens offers two cases at the length of Paul's
longer letters, where the answer is known.
- **Demosthenes and Apollodorus.** Several speeches transmitted under Demosthenes' name were written by
  Apollodorus, son of Pasion: 46, 49, 50, 52, 53, 59 (Trevett 1992; MacDowell 2009). MacDowell also gives him 45
  and 47, which others assign to Demosthenes. Can the method find Apollodorus inside "Demosthenes"?
- **Lysias, the speechwriter of many voices.** Lysias wrote speeches for clients to deliver in their own persons:
  a farmer, a disabled man, a betrayed husband, a soldier. That is ethopoeia, character-writing. Do his speeches
  still show one hand under all those characters, against other orators of his time?

The answers calibrate what the method can and cannot see when applied to Paul.

## 2. Data

Perseus canonical-greekLit; words cleaned as in the rest of the kit (accents removed).
- **Demosthenes, genuine private speeches** (reference): 27, 28, 29, 30, 31, 36, 37, 38, 39, 41, 54, 55, 57.
- **Demosthenes, genuine public speeches** (for part B only): 1-6, 8, 9, 14, 15, 16, 18-24.
- **Apollodorus** (in Demosthenes' corpus): 46, 49, 50, 52, 53, 59. **Disputed:** 45, 47, reported separately.
- **Lysias, genuine:** all speeches except 2, 6, 8, 9, 11, 15 and 20 (disputed or spurious), 33 and 34 (fragments)
  and any speech under 1,000 words.
- **Other orators:** Isaeus (all), Antiphon 1, 5, 6, Andocides 1-3, Aeschines 1-3, Isocrates 16-21 (his forensic
  speeches).
- **Paul:** the 13 letters (SBLGNT), for part C.

## 3. Method

- Each text is cut into consecutive passages of 1,000 words (the last part, if shorter, is dropped).
- Features: the 150 most frequent words in the passages of the analysis at hand.
- Distance: Cosine Delta, with z-scores over the passages of the analysis.
- **Attribution (part A):** nearest centroid, leaving out the whole speech under test. Each passage goes to the
  writer whose centroid is nearest. A speech goes to the writer with most of its passages.
- **Outlier ranking (parts B and C):** within one corpus under one name, each text's profile (its passages
  averaged) is compared with the profile of the rest of the corpus without it. The texts are ranked by that
  distance, with no labels used. The AUC says how well the ranking puts the known other hand at the top: 1.0 =
  every other-hand text ranks above every genuine text; 0.5 = no better than chance.

## 4. Tests, predictions and decision rules

**A. Lysias under many voices.** Writers: Lysias, Isaeus, Antiphon, Andocides, Aeschines, Isocrates (forensic),
Demosthenes (genuine private), Apollodorus. Attribution as in section 3; chance is 1 in 8.
- **Prediction A:** at least 60% of Lysias's passages, and at least 70% of his speeches, are attributed to Lysias.
- **Rule:** if met, writing in many characters' voices does not hide this writer's hand.

**B. Apollodorus inside Demosthenes.** The corpus is the genuine private speeches plus the six Apollodoran ones,
all private lawsuits, so genre does not separate them.
- **Prediction B1:** AUC at least 0.80 for Apollodorus against genuine Demosthenes.
- **Prediction B2:** at least 4 of the 6 Apollodoran speeches lie beyond the largest distance among the genuine
  speeches.
- **Exploratory:** where 45 and 47 fall; and the same ranking with the public speeches added.
- **Rule:** if B1 is met, a second hand of normal skill inside a famous name is visible at speech length.

**C. The same ranking on Paul.** The corpus is Paul's 13 letters. The Pastorals play the role of the known other
hand.
- **Prediction C1:** AUC at least 0.80 for the Pastorals.
- **Prediction C2:** none of the core four (Romans, 1-2 Corinthians, Galatians) ranks among the four most distant
  letters.
- **Rule:** read together with B. If the method finds Apollodorus (B) and the Pastorals (C), but does not single
  out any of the core four, that is evidence of one hand behind the core four. That is a direct test of a "school"
  writing them, at the limits stated below.

## 5. Limits stated in advance

- Attic Greek of the 4th century BCE is not Paul's Koine. Part C uses its own feature list, from Paul's letters.
- Paul's shorter letters (Titus 659 words, Philemon 334) give one passage or none; letters under 1,000 words are
  ranked on their whole text, which is noisier.
- A school that trained its writers to one house style could pass as one hand; this test cannot exclude that.
  Lysias is the check on how far a single writer's habits survive deliberate changes of voice, not on how far a
  group's habits converge.
- Authorship lists for the orators follow standard modern scholarship and need checking.
- Rules by Claude (an AI model).
