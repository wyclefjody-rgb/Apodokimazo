# One writer or a school? Can stylometry tell?

Rules written first: PREDICTIONS.md (SHA-256 6e586157…2c0e48, never edited) and AMENDMENTS.md. Results:
RESULTS.md (made by one_hand.py).

## The question

Livesey's model is a school of writers composing in Paul's voice. If that were so, the seven letters should show
more than one hand. The lineup study found them internally consistent. This study asked the prior question: can the
method see a second hand at all, when one is known to be there?

## How it was tested

Each letter collection was cut into units of whole letters. For each unit, the test asked whether its function words
stand further from the rest of its collection than one writer's letters normally do. "Normally" was measured on five
collections by single authors:
- Ignatius;
- Chion;
- the Letters of Themistocles;
- Alciphron;
- Libanius.

Then the test was tried on five cases where a second hand is known to be present:
- the Pastorals among Paul's letters;
- Hebrews among Paul's letters;
- 1 Clement among Paul's letters;
- Ignatius' letters among Paul's;
- the six forged Ignatian letters of the 4th century among the seven genuine ones.

The rule set in advance: if the method misses these, nothing it says about Paul's seven letters counts.

## Results

| known second hand | version 1 (1,000-word units) | version 2 (2,000-word units) |
|---|---|---|
| Hebrews among Paul's letters | found | found |
| 1 Clement among Paul's letters | found | found |
| the Pastorals among Paul's letters | **half missed** (1 of 2 units) | **missed** |
| Ignatius among Paul's letters | **missed** (0 of 5) | **missed** (0 of 2) |
| forged Ignatian letters among the genuine | **missed** (0 of 4) | half found (1 of 2) |
| **method works?** | **no** | **no** |

Version 1 was the method set in advance. Version 2 was written down after version 1 failed (AMENDMENTS.md 2). It
used larger units and scaled the features against the collection being tested. That too was set in advance of
running it, along with a promise not to try a third.

The method finds writers who are plainly different: Hebrews and 1 Clement. It does not reliably find writers who
are close: Ignatius, Paul's nearest neighbour in the lineup study; the Pastorals, written in imitation of Paul; and
the forger who imitated Ignatius.

Both versions flag one of Paul's units, Romans, and no other. By the decision rule that is "one hand". But since
the method failed its own tests, the rule says no conclusion is drawn.

## What this means

**1. The "one hand" argument is weaker than it looked.** At the scale of single letters, function-word stylometry
cannot separate Paul from a close imitator or a close contemporary. So the consistency of the seven letters does
not count against a school of writers, and it would not count for one either. A school that trained its members in
one voice, which is exactly what Livesey proposes, is the case this method cannot see.

**2. This cuts both ways, and it bears directly on the book.** Any claim that stylometry "proves" who wrote a single
letter, for or against Paul, faces the same limit: the method cannot reliably tell the Pastorals from Paul at this
scale. The lineup study's comparisons used whole writers' output, tens of thousands of words, which is why they
could work. Letter-level claims are a different matter.

**3. What still stands.** The lineup study still says that Paul's letters, taken together, are closest to Ignatius
and far from the 2nd-century apologists. What this study shows is how much stylometry can and cannot see. As an
argument for one writer rather than a school, the case has to rest on content (see the other studies), not on
style.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| 1. About 5% of single-author units flagged | yes: 3 of 50 (version 1), 2 of 31 (version 2) |
| 2. The sensitivity tests pass | **no**: Hebrews and 1 Clement found; the Pastorals, Ignatius and the forged letters mostly missed |
| 3. None or one of Paul's units flagged | one (Romans), in both versions; not counted, since the method failed |
| 4. The multi-author collections show more flags than single-author ones | **no**: Diogenes 1 of 7 and the Socratic letters 1 of 9 in version 1, none in version 2; Crates too short |
| 5. Ephesians and Colossians less clearly flagged than the Pastorals | neither was flagged; but the Pastorals were not clearly flagged either |

## Limits

- Units of whole letters are small; that is the point being tested, not a flaw to fix by making them bigger. Paul's
  letters are the size they are.
- Other methods might do better: more features, character n-grams, or classifiers trained on many writers. This
  study tested the method the kit uses, at its two most reasonable settings.
- The single-author collections differ from Paul in date and genre.

## Reproduce

```
python -X utf8 one_hand/one_hand.py
```

Research assistance: drafted with Claude (Anthropic).
