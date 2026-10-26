# Argument across languages, and a known forger of Paul (rhetoric_across)

Pre-registered (PREDICTIONS.md, SHA-256 76bf0f0b…a8b). Results: RESULTS.md. Rules by Claude (an AI model), for
review.

## Part 1: do a writer's argument habits survive translation? Yes, at least into the Vulgate

Twelve features of argument were measured on the Greek of the 21 New Testament letters and on the Latin of the
same letters: questions, sentence length, "by no means", "what then?", "not ... but", "if", "for", "therefore",
"it is written", "you", "we", "brothers".

- **11 of the 12 survive** (rank correlation 0.7 or more between Greek and Latin). "If" (0.97), "you" (0.96),
  questions (0.90) and "for" (0.87) carry over almost unchanged. "By no means" and "what then?" match perfectly,
  though they occur in only a few letters. Only "not ... but" falls just short (0.69).
- **Sentence length survives too (0.86),** against prediction 1. Latin sentences are shorter, because the editors
  punctuate more, but the letters keep the same order. Ephesians and Colossians have the longest sentences in both
  languages.
- **The features find each letter across the language barrier.** For 19 of the 21 Latin letters, the nearest
  Greek letter on these features is its own original (90%, against a chance level of 5%). The two misses are 2
  and 3 John, each under 300 words.

**What this does and does not show** (AMENDMENTS.md 2): these features carry a text's way of arguing through a
close translation. The Vulgate is literal, so this is a best case. It does not yet show that the features identify
an *author*. The table also shows a fact worth having for the authorship question: on argument, Ephesians and
Colossians stand apart from the core four. They have almost no questions, very long sentences, little "for" and
no "it is written".

## Part 2: the Letter to the Laodiceans (waiting for the text)

The plan: measure how much of the forgery is pasted from Paul (L1), and whether it argues like Paul (L2).

A test run on a stand-in (Paul's own Philippians 1:1-20) exposed a weakness before the real text arrived
(AMENDMENTS.md 1). Paul's real openings argue little: greeting, thanksgiving and prayer have few questions and few
"for"s. Laodiceans imitates exactly such a passage. So a low argument score alone would not prove the forger
lacked Paul's way of arguing. The results therefore compare Laodiceans with Paul's own 13 openings as well (L2b).

### How to add the text

1. Open https://bible-researcher.com/laodiceans.html. The Latin is Lightfoot's critical text (1875/1876, public
   domain).
2. Copy the 20 Latin verses only, not the English, into a plain text file, one verse per line. Verse numbers at
   the start of a line are fine; the script removes them.
3. Save it as `rhetoric_across/laodiceans.txt` (UTF-8).
4. Run the script again. It prints the file's SHA-256, so the exact text used is on record.

## Predictions against outcomes (Part 1)

| prediction | outcome |
|---|---|
| 1. At least 7 of 12 features survive; sentence length does not | 11 of 12 survive. Sentence length does too (0.86), so that half fails |
| 2. At least 50% of Latin letters find their own Greek letter | met: 19 of 21 (90%) |
| 3-5. Laodiceans | waiting for the text |

## Running it

From the kit folder, once:

    python rhetoric_across/fetch_texts.py

(It downloads the Clementine Vulgate from github.com/mborders/vulgata, MIT licence, pinned to one commit, into
rhetoric_across/vulgate/.) Then:

    python -X utf8 rhetoric_across/rhetoric_across.py

Keep rhetoric_across/vulgate/ out of public uploads, like the other source texts.
