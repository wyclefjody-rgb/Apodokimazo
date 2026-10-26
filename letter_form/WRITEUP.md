# Do Paul's letters fit ancient letters? (letter_form)

Pre-registered (PREDICTIONS.md, SHA-256 aa80ce88…250f). Generated tables: RESULTS.md and letters.csv. Measures
are automatic; the rules are by Claude (an AI model) and need review.

## The claim tested

In the Westar interview (about 13:00-14:50) Livesey says the studies that compared Paul's letters with everyday
papyrus letters "proved the reverse" of what they wanted: Paul's letters do not compare, and scholars rescued them
by saying Paul adapted the form. She reads them instead as Roman literary letters. Two questions: is the misfit
real, and is it a sign of invented letters?

## 1. The misfit is real

- **Length.** The median complete papyrus letter (1-200 CE, 301 letters with both greeting and farewell) has 51
  words, and 95% have under 156. Every one of Paul's 13 letters is longer than that. Philemon, the shortest at 334
  words, is longer than 99.7% of them; Romans (7,055 words) is 17 times the longest complete papyrus letter (399 words).
- **Formulas.** Paul never opens with the everyday χαίρειν ("greetings") and never closes with the everyday
  farewell (ἔρρωσο, "be well"). Instead all 13 letters open with "grace to you and peace" and close with a grace
  benediction. **No** papyrus letter of 1,730 has either formula (three apparent hits use χάρις for "thanks";
  AMENDMENTS.md 1).

Livesey is right about this. Paul's letters are not ordinary letters.

## 2. But the misfit is not the mark of invented letters

The best control is letters known to be invented: 613 letters from 13 Greek fictional collections (Chion,
Themistocles, the Cynic and Socratic letters, Phalaris, Alciphron and others).

| | median words | everyday greeting | grace and peace | everyday farewell | grace benediction |
|---|---|---|---|---|---|
| papyri (1,730) | 40 | 45% | 0% | 31% | 0% |
| Greek fictional letters (613) | 97 | 3% | 0% | 4% | 1% |
| Paul (13) | 1,591 | 0% | 100%* | 0% | 100% |
| Pastorals (3) | 1,235 | 0% | 100% | 0% | 100% |
| Ignatius, genuine (7) | 1,023 | 86%* | 0% | 86% | 14% |
| Greek literary letters (4) | 3,854 | 75% | 0% | 0% | 0% |
| Seneca, moral letters (124, Latin) | 720 | 100% | n/a | 100% | n/a |

\* searched in the first 150 words (RESULTS.md 6b), because Romans's and Ignatius's prescripts are long.

- **Invented letters do not look like Paul.** They are short (median 97 words), and they have none of Paul's
  Christian formulas. On the pre-registered profile they sit much nearer the papyri (distance 0.65) than Paul
  (1.97).
- **They share one thing with Paul: they also drop the everyday frame.** As printed, only 3-4% have the greeting
  or the farewell. On the frame alone the fictional letters are almost identical to Paul (RESULTS.md 6c). So
  "doesn't use the papyrus frame" is no mark of a real letter. But it is no mark of fiction either: it is shared by
  literary letters generally. One caution: this depends on how the editions print the fictional letters'
  headings.
- **Paul's frame is his own, and imitators copy it.** The grace-and-peace opening with the grace benediction is
  specific to the Pauline letters. The Pastorals, widely held to be imitations, reproduce it exactly (distance to
  the core four 0.71, to the papyri 2.18). Genuine Ignatius, writing around 110, does *not*. He uses the everyday
  χαίρειν and "be well" with Christian additions. The spurious Ignatius letters fall in between.
- **In length, Paul's long letters match literary letters.** The core four (median 5,642 words) are in the range
  of the Greek literary letters (Dionysius, Arrian; median 3,854) and 1 Clement (9,830), well above Seneca's
  moral letters (median 720 Latin words). On length, the "literary" side of Livesey's case holds up.

## What this means for the argument

- Livesey's premise holds: the papyrus comparison does show that Paul's letters are not everyday letters.
- Her inference does not follow from this evidence. The real question is whether letters written in someone
  else's name look more like Paul than real letters do. They don't. Invented Greek letters are short and carry
  no Christian frame; the Christian imitations (the Pastorals) copy Paul's frame perfectly. Form can show that a
  text belongs to the Pauline tradition. It cannot tell a real Pauline letter from an imitation, or a letter of
  the 50s from one of the 140s.
- The test is therefore neutral on date and authorship. That is a useful result in itself: arguments from letter
  form, on either side, prove less than they seem to.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| 1. All 13 longer than the papyri's 95th percentile; Philemon closest | met (13 of 13; Philemon at 99.7%) |
| 2. Under 1% of papyri have Paul's grace formulas | met (0 true cases; 3 false hits, AMENDMENTS.md 1) |
| 3. Paul's median longer than fictional and Latin literary letters, within a factor of two of Ignatius | met (1,591 against 97, Seneca 720, Pliny 163; 1.6 times Ignatius) |
| 4. Fictional letters closer to the papyri than to Paul, because they keep the everyday frame | half met: closer to the papyri (0.65 against 1.97), but not because of the frame, which they mostly lack (3-4%) |
| 5. Pastorals and spurious Ignatius closer to the core four than to the papyri | met (Pastorals clearly; spurious Ignatius narrowly, 1.58 against 1.68) |
| 6. Ignatius mixes the everyday greeting with Pauline grace language | half met: everyday greeting 6 of 7, but grace and peace 0 of 7 and grace benediction 1 of 7 |
| 7. Seneca ends nearly all letters with "vale" | met (124 of 124) |

## Limits

- Formula detection is by word lists. Long openings needed a wider window, and χάρις can mean "thanks"
  (AMENDMENTS.md 1).
- The fictional collections' greetings depend on how each edition prints headings.
- Papyrus lengths are lower bounds where text is lost; the "complete" subset helps but favours shorter letters.
- Latin is a reference only (different language, different counting).
- Only Greek prose letters with a known or conventional date are used. Christian letters on papyrus (3rd century
  and later) are not included.

## Running it

From the kit folder, once:

    python letter_form/fetch_texts.py

then:

    python -X utf8 letter_form/letter_form.py

It needs letter_period/papyri_letters_accented.json from the letter-period study (already in your kit) and sblgnt/.
