# Amendments to PREDICTIONS.md (slip-rate study)

PREDICTIONS.md is never edited (SHA-256 21f88a62ac010f19d55741155c5e67ecd617cc6d947b7abd46abdd60864c0835).

## 1. 2026-10-24: what counts as datable, made precise, and a second exposure measure (before any control was coded)

**Datable, made precise.** The slip rate per datable passage depends on how many "either" passages are counted. A
coder who lists every travel note would make every text look clean. So a passage counts only if the fact it relies on
changed between the setting and the time a later writer would be working, and can be checked against independent
evidence. That is the standard the core-four list already follows. The topics are:
- church offices;
- the names used for believers;
- the status of Jerusalem, the Temple and Judea;
- persons whose dates are known independently;
- the citing of written gospels or Christian texts as scripture;
- controversies and teachers whose dates are known;
- political offices and rulers;
- persecution by the state;
- relations with the synagogue and circumcision;
- the expectation of the end;
- predictions of later events.

Travel notes, unknown persons and places that did not change are not counted. The absence of the name "Christian" in
a text set before c. 70 is coded as in the core four ("fits the setting, weak").

**A second exposure measure.** Slips per 1,000 words is also reported. Its denominator needs no judgment. Under a
Poisson model with the Group A rate, the probability of no slip in the core four's 20,566 words is reported
alongside the per-passage figure. Length is not the same as opportunity, so this is a cross-check, not the primary
measure.

## 2. 2026-10-24: how datable passages are found, and which texts are used (before any control was coded)

**Found by search, then read.** So that every text is searched the same way, candidate passages are found by
searching the Greek for the terms in topics.txt (SHA-256 below), one list per topic of AMENDMENTS.md 1. Each hit is
shown with its verse or section, and hits in the same verse or section are read together. Each candidate is then
read and coded as "not datable" (the term is used in a way that carries no date, for example a king in a parable or a
quotation of Israel's scripture) or as one or more datable items (fits the setting / slip / either). This search is
run on Paul's core four as well. Their coded list replaces the reading-based list of vanishing_point/ as the primary
test, so that Paul and the controls are found the same way. The old list is reported alongside.

**Texts.** The kit has Greek for these texts:
- the core four, the Pastorals and 2 Peter (SBLGNT);
- the six spurious Ignatian letters (First1KGreek tlg1443.tlg002);
- the letters of Peter and Clement to James with the Contestatio (tlg1271.tlg003-005);
- the Acts of John (tlg0317.tlg001);
- the Acts of Thomas (tlg2038.tlg001);
- the Acts of Barnabas (tlg2949.tlg001).

Three texts are not in the kit's Greek: 3 Corinthians and the Acts of Paul (which survive partly in Coptic), and the
letters of Paul and Seneca (Latin). They are coded by hand from translations and reported separately, not pooled.

Group A, the primary pool, is therefore:
- the Pastorals;
- the spurious Ignatian letters;
- the Clementine letters to James.

Group B is 2 Peter and the Acts of John, Thomas and Barnabas.

topics.txt SHA-256: 1516aaeab4e1b25abaac8d63061b8234d671dbad235a23595a89d021008d166d
