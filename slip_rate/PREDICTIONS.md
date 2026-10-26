# How often do later writers slip? Predictions and rules

Written 2026-10-24, before any control text below was coded. Never edited; changes go in AMENDMENTS.md with a date.

## 1. The question

The Daniel-method study (vanishing_point/) found no passage in Romans, 1-2 Corinthians and Galatians that fits only
a time after 70. Livesey's reply is open to her: a careful writer of c. 144 could avoid every slip. This study asks
how often writers who really did write later, in the voice of an earlier figure or about an earlier time, actually
slipped, and so how surprising Paul's clean record would be if he were one of them.

## 2. The trap, and how it is handled

Most later writings we know of were exposed partly by their slips. If the slip rate is measured on them alone, it
comes out too high, because careful writers who never slipped are not on the list (survivorship bias). So the
control texts are split by **how** their late date is known:

- **Group A (late date known from outside evidence, not from slips):**
  1. **3 Corinthians**, with the Acts of Paul it belongs to. Tertullian (On Baptism 17) reports that an elder in
     Asia wrote the Acts of Paul and was removed from office.
  2. **The six spurious Ignatian letters** of the long recension (Mary of Cassobola to Ignatius, Ignatius to Mary,
     Tarsians, Philippians, Antiochenes, Hero). Eusebius (Church History 3.36) knew only seven letters, and the long
     recension is a 4th-century expansion.
  3. **The letters of Peter to James and of Clement to James**, with the Contestatio. They introduce the
     Pseudo-Clementine novel (3rd-4th century).
  4. **The letters of Paul and Seneca.** They are first mentioned by Jerome (On Illustrious Men 12, 392) and are
     usually dated to the 4th century.
  5. **The Pastorals** (1-2 Timothy, Titus). They are absent from Marcion's edition, and probably from P46.
- **Group B (late date known partly from content):**
  - 2 Peter;
  - the Acts of John;
  - the Acts of Thomas;
  - the Acts of Barnabas.

Group A is the primary control. Group B is reported alongside.

Test: Paul's core four, as already coded in vanishing_point/CHECKLIST.md after the reviewer's changes (14 datable
passages outside the passages argued to be additions; item 15, Marcion provenance, is not a dating item).

## 3. What is counted

The same rule as the Daniel-method study (vanishing_point/PREDICTIONS.md section 3). A **datable passage** is any
passage tied to a datable person, office, place, event, institution, practice, text or expectation that can be
checked against evidence independent of the text. Each is coded against the text's own setting (the time it claims
to be written, or to describe):

- **fits the setting:** fits that time and would be odd later;
- **slip:** fits only a later time (an anachronism, or knowledge of a later event, office, text or controversy);
- **either:** fits both.

Every datable passage is listed, not only slips. A passage that names a later event as a prophecy counts as a slip,
as Daniel 11 does. Purely legendary content (miracles, talking animals) is not datable and is not counted. Each code
gives its evidence. Coded by Claude, reviewed by the user, as before.

## 4. Statistics

- Slip rate of each control text = slips / datable passages.
- Pooled Group A rate r, with its uncertainty: r ~ Beta(slips + 1, non-slips + 1).
- Probability that a later writer with Group A's slip habits would produce Paul's record (0 slips in N = 14 datable
  passages): P = E[(1 - r)^N] under that Beta distribution. Reported also for Group A + B, and for the controls
  written closest to their setting (gap under 150 years: the Pastorals, 3 Corinthians and the Acts of Paul, 2 Peter,
  the Acts of John).
- Sensitivity: N = 15 counting 1 Thessalonians 2:16 as a slip (the core four plus the one strong candidate,
  1 slip in 15).

## 5. The Acts check (agreement with Acts)

For each text that tells episodes of Paul's life that Acts also tells (the Pastorals; the Acts of Paul with 3
Corinthians), every shared episode is coded as in paul_map/ (agrees, differs, conflicts). The share that agrees is
compared with the undisputed letters' share (paul_map/MAP.md: 14 of 38 episodes agree outright, 6 more add without
conflict). If the letters had been written from Acts, as Livesey proposes, they should agree with it about as often
as known later texts that drew on Acts.

## 6. Predictions

1. Every control text has at least one datable passage, and Group A's pooled slip rate is between 15% and 50% of
   datable passages.
2. Slip rates rise with the gap between setting and writing (the 4th-century texts slip more than the Pastorals).
3. P (Paul's clean record from a Group A-like writer) is below 0.05 using the pooled rate; above 0.05 using only the
   closest-in-time controls is possible, because they are few and short.
4. The later texts that tell Paul's story agree with Acts more often than the undisputed letters do.
5. Overall: Paul's record is unusually clean for a later writer, but the closest-in-time comparison is too small to
   make it decisive.

## 7. Limits stated in advance

- Survivorship bias is reduced by Group A, not removed: even Group A texts are the later writings that survived and
  were recognized.
- The control texts are fewer and shorter than Paul's letters, so the rates are rough.
- The apocryphal Acts are novels, a different genre from letters; that is why they are Group B.
- Coding is judgment and needs review.
