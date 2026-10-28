# Did the coder's knowledge make the slip test work? A blind check

Pre-registered (PREDICTIONS.md, SHA-256 f7b89d0c…0c4e). Results: RESULTS.md. Decisions: AMENDMENTS.md 1-2.

## The question

The slip test (slip_rate, third_corinthians, real_letters) was coded by one coder who knew which letters were
genuine. Its main weakness: a coder who expects forgeries to slip may find slips, and excuse them in genuine letters.

## What was done

All 158 datable items from the three studies were put in one shuffled list (SHEET.md). Each line gives only:
- the claimed date;
- the detail, with the letter-writer's own name replaced by "the writer".

There are no titles, groups or original codes. Two fresh AI coders, each seeing only the sheet, coded every item
fits / either / slip / not.

## Results

| coder | genuine letters | Group A + 3 Cor | Group B | Paul's core four | ratio for Paul's record |
|---|---|---|---|---|---|
| original (not blind) | 0/59 | 18/51 (35%) | 6/32 (19%) | 0/16 | 347 to 1 |
| blind coder 1 | 0/59 | 24/49 (49%) | 11/30 (37%) | 0/16 | about 6,500 to 1 |
| blind coder 2 | 0/59 | 22/45 (49%) | 13/29 (45%) | 0/16 | about 5,700 to 1 |

- Agreement with the original coding on slip / not slip: kappa 0.65 and 0.69.
- Agreement between the two blind coders: 0.85.
- **All five predictions were met by both coders.**

## What it means

- **The original coder was not too harsh on the forgeries; if anything, too lenient.** The blind coders found
  more slips in the later writings, not fewer. They flagged 15 items the original had passed (for example, 3
  Corinthians putting Paul's chains at Philippi after he founded Corinth, against Acts).
- **Neither blind coder found a slip in a genuine letter or in Paul.** The separation the slip test relies on held
  without the original coder's knowledge of the groups.
- The higher slip rates make the ratios for Paul's record larger. The registered result stays the conservative 347
  to 1.

## Limits

- **Not truly blind.** The coders recognised sources (their reasons cite Acts and 1 Corinthians), and an AI knows
  which letters are famous and genuine. What was hidden was the grouping, not the texts.
- **Same kind of coder.** The blind coders are AI models like the original coder and may share its blind spots.
  Your own hand coding is the stronger check: your_codes.txt.
- **Items were chosen and described by the original coder.** The blind coders judged the details given, not which
  details to pick.
- **No web checks.** The blind coders coded from knowledge; their reasons are unverified.

## Running it

    python -X utf8 blind_check/make_sheet.py
    python -X utf8 blind_check/blind_check.py

make_sheet.py needs slip_rate/, third_corinthians/ and real_letters/ in the kit. To add your own coding, fill in
your_codes.txt (`B001 | code | strength | reason`) and save it as blind_check/coders/your_name.txt. Don't look at
key.csv or the coders folder until you are done.
