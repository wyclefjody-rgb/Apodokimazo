# 3 Corinthians, a known forgery in Paul's name

Pre-registered (PREDICTIONS.md, SHA-256 32147012…f277). Results: RESULTS.md. Text preparation and reading:
AMENDMENTS.md 1-2. Coding by Claude (an AI model), for review. Text: Vouaux, Les Actes de Paul (1913), the user's
scan.

## Why this text

3 Corinthians is an exchange: a letter from the Corinthians to Paul, and Paul's reply, written from prison in
Philippi. It is a 2nd-century forgery, and we know that from outside evidence: Tertullian (On Baptism 17, c. 200)
says the Acts of Paul, which contain it, were written by a presbyter of Asia who was removed from office for it. So
it is a fair test case for two earlier studies.

## Part A: it slips, as later writers usually do

8 datable items, **4 slips** (2 medium, 2 weak): a slip rate of 50%, or 25% without the weak ones.
- **The apostolic tradition (medium).** Paul says he handed on what he "received from the holy apostles before me,
  who were with the Lord all the time". The real Paul swears the opposite: his gospel came "not from any human
  being" (Galatians 1:11-12). The forger gave Paul the 2nd century's concern with apostolic succession.
- **The heresy (medium).** Simon and Cleobius teach a whole Gnostic system in Corinth: the prophets rejected, the
  world made by angels, Christ not truly in the flesh nor born of Mary, no resurrection of the flesh. Parts have
  1st-century roots (1 Corinthians 15:12 already has resurrection deniers), but the combined system is that of the
  2nd-century teachers.
- **Elders (weak)** leading the church with Stephanas, and **a "rule" received through the prophets and the holy
  Gospel (weak)**, the later language of a rule of faith.

**What it adds to slip_rate.** 3 Corinthians was the closest-in-time control with an outside date that slip_rate
could not code. Added to the controls, the chance that a later writer would be as clean as Paul's four main letters
(0 slips in 16 items) goes down, not up: 0.0023 (it was 0.0043). Added to the controls closest in time, it is 0.0099
(it was 0.031). Here is a forger writing in Paul's own voice, to Paul's own church, and in a few hundred words he
contradicts Galatians and imports his own century's controversy.

## Part B: style in Latin does not catch it

The Latin text of 3 Corinthians (647 words) and Paul's side of the Paul and Seneca letters (452 words) were measured
as Laodiceans was in rhetoric_across.
- **Shared wording:** 3 Corinthians shares only 3.3% of its 3-word sequences with the Vulgate's Paul, below a
  typical passage of Paul (6.7%). Its Latin is an older translation made independently of the Vulgate, so exact
  wording undercounts its borrowing (it does take "vinctus Christi Jesu" and "stigmata ... in corpore meo porto"
  from Paul). Paul to Seneca shares 1.6%.
- **Argument:** both forgeries score inside Paul's normal range on the argument score (3 Corinthians 29.4, Paul to
  Seneca 46.5; Paul's passages: 5th percentile 12-15, median 47-50). Even Paul to Seneca, polished literary Latin
  that does not imitate Paul at all, looks like Paul by this measure.

So B1 and B3 fail. The argument score counts words like "if", "for", "therefore", "not ... but", which any Latin
argument uses. Across a translation, it does not tell Paul from a forger, even a forger who did not try.

## What it means

- **Content catches forgers where style does not.** 3 Corinthians slips four times in about 650 words, while the
  style measures cannot even tell Paul to Seneca from Paul. That matches the rest of the kit: one_hand and
  rhetoric_across showed style failing at letter length; slip_rate and vanishing_point showed content working.
- **It strengthens the slip-rate argument.** The Livesey model needs writers of about 144 who made no slip across
  16 datable points. The one known 2nd-century forger of a letter by Paul to Corinth, writing a generation or so
  later, made four in 8.
- **The limits:** one more text, coded by an AI model; 3 Corinthians may be a little later than 144 (usually
  c. 150-190); and the Acts of Thomas remains the warning that some later writers are careful.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| A1. At least one slip | met: 4 |
| A2. Slip rate between 15% and 50% | met at the edge: 50% (25% without weak slips) |
| A3. With 3 Corinthians in Group A, P stays below 0.05 | met: 0.0023 |
| B1. 3 Corinthians above Paul's median share, not above every passage | not met: 3.3% against a median of 6.7% (independent Latin translation) |
| B2. 3 Corinthians' argument score within Paul's range | met: 29.4 (5th percentile 12.1) |
| B3. Paul to Seneca below Paul's median share and below his 5th percentile on argument | half: share 1.6% (below), argument 46.5 (not below) |

## Running it

From the kit folder, with rhetoric_across's Vulgate already fetched and slip_rate present:

    python -X utf8 third_corinthians/third_corinthians.py

Keep third_corinthians/texts/ out of public uploads (AMENDMENTS.md 1).
