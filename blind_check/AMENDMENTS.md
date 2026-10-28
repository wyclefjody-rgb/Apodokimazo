# Amendments to PREDICTIONS.md (blind_check)

PREDICTIONS.md is never edited (SHA-256 f7b89d0c659761ceeb7b68ef3a97b0ce15726a2a2c58b1f282c2826a72920c4e).

## 1. 2026-10-27: decisions made before any blind code was seen

- **Names hidden.** Only the letter-writer's own name is replaced by "the writer" (Paul in the core four and 3
  Corinthians; Pliny, Cicero, Seneca; Ignatius in the spurious Ignatian letters; Clement in the Clementine letters).
  A first draft replaced every occurrence of these names in every item, which turned "Paul and Barnabas" in the
  Acts of Barnabas into "the writer and Barnabas" and so changed the claim. Fixed before the sheet went to any
  coder. Other people keep their names.
- **Sheet:** 158 items, shuffled with seed 20261027 (make_sheet.py). Each line gives the claimed (or known) date of
  writing or setting, never the title.
- **Coders:** two fresh AI agents, each given only SHEET.md and told not to open any other file; free to search the
  web. Their answers are copied unchanged to coders/ai_coder_1.txt and coders/ai_coder_2.txt.
- **Slip rates** use, as denominator, the items each coder codes fits, either or slip (a blind coder may code an
  item "not").
- **Prediction 5 when Paul's record is not clean.** real_letters' ratio assumes 0 slips. If a blind coder finds s
  slips in Paul's N items, the ratio is the beta-binomial chance of exactly s in N under the genuine rate, divided
  by the same under the later rate. With s = 0 this is the same number as before (checked: the original codes give
  347 to 1).

## 2. 2026-10-27: after the blind codes came in

- **Coder 1 did not use web search;** it coded from its own knowledge. Coder 2 also worked from knowledge (two
  tool calls: read the sheet, write the answers). Neither checked citations, so their codes are judgements, not
  verified evidence. Both files are kept unchanged.
- **The coders recognised many sources.** Their reasons name Acts, 1 Corinthians and Paul. The sheet hid the
  grouping, not the identities (as section 5 of PREDICTIONS.md expected).
