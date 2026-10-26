# Which came first, Acts or Paul's letters?

Rules written first: PREDICTIONS.md (SHA-256 d285a3a1…cb8bcb, never edited) and AMENDMENTS.md. Results: RESULTS.md
(made by acts_order.py) and CHECKLIST.md (hand-coded).

## Why it matters

Livesey holds that Acts came first and invented Paul, and that the letters were written in his voice around 144, partly
to correct Acts. On the usual view the letters came first (50s) and Acts later. The Paul map showed that the two
conflict, but a conflict alone does not show who answered whom.

## The method

When one writer copies another, the source's habits of language leak into the copy where it follows the source.
Luke's use of Mark is the textbook case, and it is used here as the positive control.

A writer's **characteristic words** are those he uses at least four times as often as the rest of the New Testament
does. The lists are built only from passages that are not being tested. Proper names are left out.

## Results

| test | finding | ratio | p |
|---|---|---|---|
| C. Do Mark's words show where Luke copies Mark? (control) | **yes**: the method can see known copying | 1.71 | 0.0001 |
| D1. Do Paul's speeches in Acts use the letters' words more than Acts' other speeches do? | **yes** | 1.57 | 0.0009 |
| D2. Do the letters' life-story passages use Acts' words more than the rest of the letters? | **no** | 1.07 | 0.39 |
| G. Genre control: the letters' other narrative passages | no | 0.66 | 0.81 |

Under the reading set in advance, D1 "yes" with D2 "no" means two things:
- Acts' writer knew Paul's way of speaking.
- There is no sign that the letters knew Acts' way of speaking.

That fits the letters coming first.

**Checks on D1.** These were added after the run and are labelled exploratory:
- **The word ἀνήρ.** It inflated D1, because of the speech formula "Men, brothers!" (ἄνδρες ἀδελφοί). Without it, D1
  still holds: p = 0.007 against all other speeches, and p = 0.0015 against Peter's speeches only. (With ἀνήρ kept,
  the comparison with Peter's speeches alone gives p = 0.08, because Peter also uses the formula.)
- **Words both writers favour.** Some of the "Pauline" words are favoured by Luke as well (σύν, εὐαγγελίζω). Using only
  words that are Pauline and not Lukan, the share of such words rises steadily as Acts turns to Paul:

  | text | Pauline-only words |
  |---|---|
  | Luke | 0.86% |
  | Acts 1-12 narrative | 0.88% |
  | Acts' other speeches | 1.28% |
  | Acts 13-28 narrative | 1.63% |
  | Paul's speeches in Acts | 1.75% (p = 0.019 against the other speeches) |

  Part of this is topic: law, circumcision, idol food and letters themselves. Part is Paul's theological vocabulary:
  justify, righteousness, grace, hope, conscience.

**Check on D2.** With a looser threshold (2 instead of 4), D2 reaches p = 0.016. Almost all of that comes from the
preposition πρός, which Luke uses heavily. D2 is null at the pre-registered threshold and at the stricter one.

**Shared phrases (A2).** Acts shares 255 rare three-word phrases with the letters; Luke, by the same author and of
the same length, shares 164. Most are generic. Reading the list turns up a few real points of contact:
- "through the wall" in the basket escape (Ac 9:25 / 2Co 11:33);
- "being a zealot" (Ac 22:3 / Ga 1:14);
- "Syria and Cilicia" (Ac 15:41 / Ga 1:21);
- "Macedonia and Achaia";
- Troas.

Found in the hand reading: the verb "ravage" (πορθέω), of Paul attacking the church, occurs in the New Testament
only in Ga 1:13, 1:23 and Ac 9:21.

**Hand-coded pairs (Part B, 14 items).** The result is mixed:
- **Acts looks like the later telling (4 items: 2 medium, 2 weak).** The strongest is the collection. Acts keeps
  unexplained traces of it (seven delegates appear from nowhere; "alms to my nation" is mentioned in passing), and
  only the letters explain them.
- **The letters look like the later telling (3 items: 1 medium, 2 weak).** The strongest is the first visit to
  Jerusalem. Galatians' sworn denial matches claims that only Acts makes: Barnabas bringing Paul "to the apostles",
  and Paul preaching "throughout Judea".
- **No direction (7 items).**

## What this shows, and what it does not

- **The two texts are in contact.** The shared rare wording rules out independence: the basket "through the wall",
  "being a zealot", and "ravaged".
- **The language evidence points one way.** Acts' writer's vocabulary moves toward Paul's when he writes about Paul.
  The letters show no sign of Luke's vocabulary where they tell the same events. This is the same kind of evidence
  that shows Luke copied Mark, and it fits the letters, or at least Paul's own way of speaking, coming before Acts.
- **The reverse order has a gap to explain.** If Acts came first and the letters were written from it, the letters'
  rich and consistent idiom did not come from Acts. The letters have 154 characteristic words; Acts' Paul uses 24 of
  them, at about a fifth of the letters' rate (1.75% against 9.07%). The letter-writers would have had to supply Paul's voice themselves, while
  avoiding Luke's.
- **It does not prove the letters were written in the 50s.** Acts' writer could have known Paul's idiom from his
  followers rather than from letters. And if Acts is as late as Livesey's 144, the result fits a Paul whose letters
  were older than Acts, but says nothing about how much older.
- **It does not settle the direction of every episode.** The hand-coded pairs split. On the first Jerusalem visit,
  Galatians really can be read as answering Acts.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| 1. The Mark control works | yes (p = 0.0001) |
| 2. D1 positive, mostly in the Antioch and Miletus speeches | positive (p = 0.0009); but spread across the speeches, highest in the Areopagus speech and the Rome speech of 28:17-20 |
| 3. D2 not above the genre control | yes |
| 4. Acts shares more exclusive phrases than Luke, few and mostly topical | yes (255 vs 164), mostly generic |
| 5. Part B mixed, nothing decisive | yes (4 / 3 / 7) |
| 6. Leans letters-first, does not exclude Livesey | yes |

## Limits

- The passages are short: Paul's speeches in Acts are about 2,200 words; the letters' life-story passages about 1,750.
- Topic explains part of D1. Speeches about the law will use the word "law".
- The leakage logic tests contact with a writer's language, not with a written text.
- Part B is judgment by Claude (an AI model) and needs a second reader, like the earlier checklists.

## Reproduce

```
python -X utf8 acts_order/acts_order.py
```

Research assistance: drafted with Claude (Anthropic).
