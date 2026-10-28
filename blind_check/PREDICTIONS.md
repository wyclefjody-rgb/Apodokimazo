# Blind check of the slip coding: predictions and rules

Written 2026-10-27, before the blind sheet was made or any blind coder saw it. Never edited; changes go in
AMENDMENTS.md with a date.

## 1. Why

slip_rate, third_corinthians and real_letters were coded by one coder (Claude) who knew which texts were genuine
and which were later. A coder who expects a forgery to slip may find slips; one who expects a genuine letter to be
clean may excuse its errors. This check repeats the coding with coders who are not told which is which.

## 2. Design

- **Items:** every datable item already coded fits, either or slip in real_letters/codes.txt (Pliny, Cicero,
  Seneca), slip_rate/codes.txt (Paul's core four, Groups A and B) and third_corinthians/codes.txt.
- **The blind sheet:** each item becomes one line: an ID, the date the letter claims to be written (or is known
  to be written), and the detail as described in the codes. Not shown: the title, the author's name where it is
  the writer of the letter (replaced by "the writer"), the original code, the reason, the group. Order: shuffled
  with a fixed seed. The key (ID to text and original code) is kept in a separate file that coders do not see.
- **Coders:** two fresh AI agents that have not seen this project, each working alone from the sheet and the
  coding rule (slip_rate's: fits / either / slip / not, with a reason), and free to look things up. Later, the
  user codes the same sheet by hand; that is a third, human coder.
- **Scoring (blind_check.py):** for each coder, the slip rate of each group (genuine letters, Group A + 3
  Corinthians, Group B, Paul's core four), agreement with the original codes (Cohen's kappa on slip / not slip),
  and real_letters' likelihood ratio recomputed with the blind codes.

## 3. Predictions

1. Each blind coder finds a slip rate below 10% in the genuine letters.
2. Each blind coder finds a slip rate of at least 15% in Group A + 3 Corinthians.
3. Each blind coder finds at most 1 slip in Paul's 16 items.
4. Kappa between each blind coder and the original coding, on slip / not slip, is at least 0.5.
5. With each blind coder's codes, the likelihood ratio for Paul's record (genuine : later, as in real_letters) is
   above 20.

## 4. Decision rule

- If 1-3 and 5 hold for both coders: the slip results do not depend on the original coder knowing the answer.
- If a blind coder finds genuine letters slipping at 10% or more, or later writings below 15%, the slip test's
  separation was partly the coder's expectation, and the earlier results are weakened accordingly. Reported either
  way.

## 5. Limits stated in advance

- **Not fully blind.** Many details identify their source (Trajan, Atticus, Simon and Cleobius), and an AI coder
  knows from general knowledge which famous letters are genuine. What is hidden is the grouping and the original
  code, not the texts' identities.
- **Items were chosen by the original coder.** The blind coders judge the items, not which details count as
  items. A detail the original coder skipped is not tested.
- The item descriptions are the original coder's words; they can carry framing.
- AI coders share training with the original coder; the human coding is the stronger check.
