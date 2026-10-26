# One writer or a school? Predictions and rules

Written 2026-10-23, before any distance below was computed (only the word counts of the collections were looked at,
to set the unit sizes). Never edited; changes go in AMENDMENTS.md with a date.

## 1. The question

Livesey's mechanism for the letters is a school: several writers around Marcion composing in Paul's voice, as the
Roman schools trained students to do (prosopopoeia). That predicts more than one hand in the seven letters. The
lineup study found them internally consistent, but did not test whether the method can see several hands writing in
one voice. This study does that, with letter collections whose authorship is known or widely agreed.

## 2. Texts

Greek from SBLGNT (New Testament) and First1KGreek (everything else), read letter by letter.

- **Test:** Paul's seven undisputed letters, in the order Ro, 1Co, 2Co, Ga, Php, 1Th, Phm.
- **Single-author letter collections (calibration):**
  - Ignatius, the seven letters of the middle recension (tlg1443.tlg001);
  - Chion of Heraclea, an epistolary novel usually judged the work of one author (tlg0041);
  - the Letters of Themistocles, usually judged one author (tlg0055);
  - Alciphron, one author writing in many invented voices (tlg0640);
  - Libanius, his letters in order up to 20,000 words (tlg2200).
- **Known second hands (sensitivity):** each is added to a collection, and the method must flag it.
  1. the Pastorals (1Ti, 2Ti, Tit) among Paul's letters (a later writer imitating Paul, in most critical judgment);
  2. Hebrews among Paul's letters (a different writer, once counted as Paul's);
  3. 1 Clement among Paul's letters (a different writer of the same genre and period);
  4. Ignatius' seven letters among Paul's letters (the lineup study found him Paul's nearest neighbour in style);
  5. the six spurious letters of the long Ignatian recension (Mary of Cassobola to Ignatius, Ignatius to Mary,
     Tarsians, Philippians, Antiochenes, Hero; tlg1443.tlg002), a 4th-century writer imitating Ignatius, among
     the seven genuine letters.
- **Collections widely held to have several authors (descriptive):**
  - the Letters of Diogenes (tlg1325);
  - the Letters of Crates (tlg0623);
  - the Socratic letters: Socrates and the Socratics together (tlg0636 + tlg0637).
- **Reported alongside, not decisive:**
  - Ephesians, Colossians and 2 Thessalonians among Paul's letters;
  - the Letters of Phalaris (authorship debated).

## 3. Method

1. **Words** are written in the kit's function form (paul_lineup/words.py). The features are the 100 most frequent
   words of paul_lineup/features/function_words.txt, each collection weighted equally.
2. **Units:** letters are taken in collection order. Consecutive letters are joined until a unit has at least 1,000
   words. A short remainder at the end joins the last unit.
3. **Blocks:** each unit is cut into blocks of 500 words; a remainder under 500 is dropped.
4. **Profiles:** each block's rates are z-scored with the mean and spread over all blocks of the study. Distance is
   cosine distance (Cosine Delta).
5. **Outsider ratio** of a unit U in its collection C:
   R(U) = mean distance from U's first two blocks to every block of C's other units, divided by the mean distance
   between blocks of C's other units that belong to different units. R near 1 means U is as typical as the rest; a
   high R means U stands apart. Using only the first two blocks keeps every unit the same size (1,000 words), so
   long letters are not favoured.
6. **Threshold:** the 95th percentile of R over every unit of the five single-author collections. A unit above it
   is "flagged". In a single-author collection about 1 unit in 20 is flagged by chance.
7. **Robustness (reported, not decisive):** for Paul's long letters, R for every two-block window, not just the
   first.

## 4. Decision rules

- **The method works** only if, in the sensitivity tests:
  - both Pastoral units are flagged;
  - Hebrews and 1 Clement are flagged;
  - at least half of the Ignatius units among Paul's letters are flagged;
  - at least half of the spurious Ignatian units among the genuine ones are flagged.
  If the Pastorals are not flagged, the method cannot see an imitator of Paul and no conclusion is drawn about the
  seven letters.
- **Several hands in the seven letters:** two or more of Paul's six units flagged. **One hand:** at most one
  flagged (one could be chance).

## 5. Predictions

1. About 5% of the single-author units are flagged (by construction).
2. The sensitivity tests pass: the Pastorals, Hebrews and 1 Clement are flagged, and so are most of the Ignatius
   units and most of the spurious Ignatian units.
3. Of Paul's six units (Ro, 1Co, 2Co, Ga, Php, 1Th with Phm), none or one is flagged.
4. The multi-author collections (Diogenes, Crates, Socratic) have more flagged units than the single-author
   collections. Their internal authorship is not known letter by letter, so this is descriptive only.
5. Ephesians and Colossians are not flagged as clearly as the Pastorals; 2 Thessalonians is too short to tell
   (under 1,000 words, so it joins nothing and is reported as too short).

## 6. Limits stated in advance

- A school that edited every letter into one house style could pass as one hand. The spurious Ignatian letters and
  the Pastorals show how far real imitators got. They are the best available test of that, not a proof.
- Units of 1,000 words are small for function-word stylometry; the threshold is calibrated at that size.
- The single-author collections are different in date and genre from Paul; the calibration measures how much one
  writer varies across letters, not how much Paul should.
