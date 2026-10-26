# Amendments to PREDICTIONS.md (one-writer study)

PREDICTIONS.md is never edited (SHA-256 6e58615717e4edd6ca407364ffe9a077798b359b70219e2ce10ed565fb2c0e48).

## 1. 2026-10-23: bug fix (after the first run)

A collection with only two units (Crates) has no pair of "other units" to compare, so R was undefined (shown as
"nan"). Such collections are now reported as "too few units". No other result changes.

## 2. 2026-10-23: the first method failed its sensitivity tests; a second version (written before it was run)

The first run failed the rule of section 4. Among Paul's letters it flagged Hebrews and 1 Clement, but only one of
the two Pastoral units. It flagged none of Ignatius' units and none of the spurious Ignatian letters. By the rule
set in advance, no conclusion is drawn from it about the seven letters, and its results stay in RESULTS.md as the
first version.

A second version is set out here before it is run. It changes three things, each a standard choice that the first
version did not make:
1. **z-scores are computed over the blocks of the collection being tested** (the host collection plus anything
   added), not over every block of the study. This is the usual practice in Delta: features are scaled against the
   texts being compared, so that differences between similar writers are not drowned by the much larger
   differences between, say, Alciphron and Libanius.
2. **Units of at least 2,000 words, and R uses each unit's first four blocks** (2,000 words) instead of two. Paul's
   units become Ro, 1Co, 2Co, Ga, and Php + 1Th + Phm. Libanius is read up to 40,000 words instead of 20,000, so
   that the calibration still has enough units.
3. Everything else (features, blocks of 500, the threshold at the 95th percentile of single-author units, and the
   decision rules of section 4) is unchanged. The first version's predictions apply to the second.

If the second version also fails its sensitivity tests, that is the finding: at the scale of single letters, this
kind of stylometry cannot tell a close second hand from the first. In that case the consistency of the seven letters
(the lineup study) cannot be used as evidence against a school of writers, or for one. No third version will be
tried.
