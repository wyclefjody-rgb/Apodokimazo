# Paul outside Marcion's circle, to about 160

Pre-registered (PREDICTIONS.md, SHA-256 176087ea…13b7db). Results: RESULTS.md. Every candidate: CANDIDATES.md, coded
in codes.txt (uses) and not_uses.txt (with reasons). Changes and decisions: AMENDMENTS.md 1-2. Coding by Claude (an
AI model), for review.

## The question

If Marcion's school wrote Paul's letters around 144, then by about 160 they were at most some 15 years old and came
from one Roman group. So: did Marcion's rivals use Paul by then, and was their Paul fuller than Marcion's edition?

## The witnesses

| witness | group | usual date | what survives |
|---|---|---|---|
| Valentinus | Valentinian | c. 136-160 | 6 short fragments quoted by Clement (373 words) |
| Basilides and his son Isidore | Basilidian | c. 117-150 | 7 short fragments quoted by Clement (537 words) |
| Ptolemy, Letter to Flora | Valentinian | c. 150-160 | the whole letter, in Epiphanius (2,003 words) |
| Justin | anti-Marcionite, Rome | c. 150-160 | both Apologies and the Dialogue (69,752 words) |
| Basilidians in Hippolytus (tier 2) | Basilidian | source undated; Hippolytus c. 225 | Refutation 7.20-27 |
| Theodotus (tier 2) | Valentinian | c. 160-170 | Clement's Excerpts from Theodotus |

The Epistle of the Apostles and the Coptic Nag Hammadi texts are not coded yet (AMENDMENTS.md 1).

## What was found

**1. A Valentinian teacher quotes Paul by name, including the anti-Marcionite verse.** Ptolemy names "Paul the
apostle" and quotes three letters: 1 Corinthians 5:7, Ephesians 2:15 and Romans 7:12 ("the law is holy"). He also
echoes 1 Corinthians 8:6, "the Father, from whom are all things". That verse is one of the strongest in our
marcion_text study: Marcion's own edition kept it although it speaks against him. Ptolemy is neither Marcionite nor
catholic, and he treats Paul as an authority he shares with his reader.

**2. Justin uses Romans 11, a chapter Marcion's edition lacked.** In Dialogue 39.1, Justin quotes Elijah's
complaint in Paul's form, not the Septuagint's:
- prophets killed before altars torn down (the Septuagint has the reverse order);
- "and I alone am left" (κἀγὼ ὑπελείφθην μόνος, against the Septuagint's ὑπολέλειμμαι ἐγὼ μονώτατος);
- "who have not bowed the knee to Baal" with Paul's feminine article (τῇ Βάαλ).

He also has Paul's forms of Galatians 3:10 and 3:13, of Ephesians 4:8 ("he gave gifts to men"), and of the chain
of verses in Romans 3:10-18. He never names Paul. This is the one tier-1 use of a passage Marcion's edition lacked,
so by the rule set in advance it is good evidence that a fuller Romans was in his rivals' hands by about 155-160.

The caution, stated in advance: Justin may have taken these quotations from a collection of proof texts rather than
from Romans itself. His reply line ("there are still seven thousand men to me") does not follow Paul's wording
exactly. If the collection took the form from Romans, Romans 11 still existed; if Paul and Justin both took it from
an older collection, Justin does not show Romans 11 existed.

**3. The Valentinians' Paul had the passages Marcion lacked.** In Theodotus (c. 160-170), the Valentinians quote:
- Romans 8:20-21 as "the apostle", on creation subjected to futility;
- Romans 11:16-26 (the olive tree, "and so all Israel will be saved");
- Colossians 1:16 ("in him were created the things visible and invisible").

All three are in passages Marcion's edition lacked. The Basilidians in Hippolytus quote Romans 8:19-22 "as it is
written", treating Paul as scripture. These are tier 2: later, or reported by an opponent.

**4. Nobody outside the catholics uses the Pastorals.** No tier-1 or tier-2 witness has a Q, V or A use of 1-2
Timothy or Titus. That fits the Pastorals being a catholic addition, and it fits both the usual dating and
Livesey's.

**5. The earliest fragments say almost nothing.** The 910 words of Valentinus, Basilides and Isidore have no clear
use of Paul. One allusion (Valentinus: "the law written in the heart", Romans 2:15) is the closest.

## What this means for Livesey

- **It narrows her window further.** On her model, by about 155-160, letters just composed in Marcion's school
  were already being quoted in a fuller form by his enemy Justin in Rome, and by name, as an apostle's, by the
  Valentinian Ptolemy.
- **Her model can absorb part of this.** Livesey can argue that the catholic text, with Romans 9-11, was produced
  quickly in the 150s against Marcion. Justin knowing Romans 11 by 155-160 would fit that.
- **The Valentinian evidence is harder for her.** The Valentinians were neither Marcionites nor catholics. By about
  160-170 their Paul had the passages Marcion lacked (Romans 8:20, Romans 11, Colossians 1:16), quoted as their own
  apostle's text. If those passages were a catholic addition of the 150s, a rival group adopted them within a few
  years, and the Valentinians were in Rome too, so it is possible. But it means the fuller Paul was common property
  of three rival groups within about 25 years of 144.
- **It does not prove an early date.** Everything here is after 144 on the usual dates. It shows how widely Paul was
  shared, and in what form, not when he wrote.

## Predictions against outcomes

| prediction | outcome |
|---|---|
| 1. At least 3 of 5 tier-1 witnesses have a Q or V use | not met: 2 (Ptolemy, Justin); provisional, the Epistle of the Apostles is not yet coded |
| 2. Ptolemy names Paul and quotes at least two letters | met: three (1 Corinthians, Ephesians, Romans) |
| 3. A tier-1 Q, V or A use of class B, C or D | met: Justin, Dialogue 39.1 ~ Romans 11:3-4 (V) |
| 4. Tier 2 has at least 3 Q or V uses of class B, C or D | met: 6 (Theodotus 4, Hippolytus' Basilidians 2) |
| 5. Justin never names Paul | met |

## Limits

- Few tier-1 texts survive. Valentinus and Basilides are known from under 1,000 words, chosen by Clement for his
  own purposes.
- Justin's Pauline forms may come through a proof-text collection (section 2 above).
- The usual dates are standard ranges and need checking. Theodotus and the Basilidians in Hippolytus cannot be dated
  closely.
- The non-Greek witnesses are not yet coded (AMENDMENTS.md 1).
- Coding is by an AI model; every use and every rejected candidate has its reason written down.

## Running it

    python rival_witnesses/fetch_texts.py
    python -X utf8 rival_witnesses/rival_witnesses.py
