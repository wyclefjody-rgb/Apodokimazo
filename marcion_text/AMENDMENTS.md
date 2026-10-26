# Amendments to PREDICTIONS.md (marcion_text)

PREDICTIONS.md is never edited (SHA-256 3c8dfa4bfd3543d4352158ecd60ee8916f118c1116af02227e3c14edac1ff3c7).

## 1. 2026-10-24: how "against on its face" was applied (during coding, before the first tally)

Section 3 defines "against on its face" by what the passage's own words do. Applying it needed a line for
quotations of Israel's scriptures, because Marcion (on Litwa's reading) accepted those scriptures as the Creator's
own. The line used:
- **strong:** the letter's own words identify its God or Christ with the Creator, or with Israel's history or
  scripture ("one God, the Father, from whom are all things"; "the God who said, Let light shine out of darkness";
  "the rock was Christ"; "it was written for our sake").
- **medium:** Israel's scripture or law is cited *with a formula* ("it is written", "the law says") as the authority
  for what the letter's God does or what Christians must do; or the law is called holy and good.
- **weak:** the same without a formula, or where the identification needs one step of inference.
- An unmarked quotation that a reader would not recognise as scripture is coded "by argument", even when Tertullian
  points out its source.

The decision rule is applied as pre-registered, counting every "face" code. The three strength tiers, and the
"attested" column (whether Tertullian *says* Marcion kept a passage, or only argues from it), were added during
coding as exploratory checks. They are reported as sensitivity rows in TERTULLIAN.md, not as a new rule.

## 2. 2026-10-24: units and chapter numbering

- A code covers one passage as Tertullian treats it. A long passage he treats as one unit (1 Cor 7) is one code.
  1 Cor 10:1-4 and 10:6-11 are two codes because they make separate claims: the first makes the wilderness rock
  Christ, the second says Israel's story "was written down for our instruction". Merging them would give 16
  "in, face" passages instead of 17.
- The Perseus file has no division for chapter 9 of Book 5. tertullian.py splits it off at Oehler's own marker
  ("Cap. IX."), so chapters are numbered as in printed editions.
- Each code carries a few Latin words from the chapter it cites; the script refuses to run if any is missing.
  Oehler's marginal references to Paul are listed when no code covers them, so omissions are visible. The 27
  listed on the first run were all checked by hand: each is a passing cross-reference (for example Galatians 4:4
  recalled in the 1 Corinthians chapters), not a passage Tertullian discusses as part of Marcion's text of that
  letter.

## 3. 2026-10-24: note on prediction 5

Prediction 5 named two examples to check: Romans 1:3 and Galatians 4:4 ("born of a woman, born under the law").
Romans 1:3 is not discussed in Book 5 at all. Galatians 4:4b is coded "unclear": Tertullian quotes 4:4a and goes
straight to 4:5, twice, which suggests the words were missing from Marcion's text. Neither example counts toward
the total.
