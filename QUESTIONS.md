# Questions for Christ Before Jesus

Ordered from strongest to weakest. Each one gives the question, why it matters, what the kit shows, where to find that on your own computer, what they'll probably say back, and where the book says it.

**About the citations:** "Ch." is the chapter and the quoted words are the book's section headings, which are the same in every edition. Page numbers are Kindle page numbers ("Page X of 316") and appear only where they were visible in the screenshots. Print editions may be numbered differently.

Their book invites this in Chapter 7 ("Stylo Demo" introduction, Kindle p. 209): *"If you want to repeat our tests, try to disprove us, or improve upon what we've done and make further discoveries, you can. If we are wrong or lying, you can catch us."* That's the tone to keep. You're taking them up on it.

---

## Start with what they got right

Conceding these first makes the rest harder to wave away.

- Stylometry does pick up real style. The closest chapter comes from the same book 52% of the time, against about 10% for shuffled words.
- Luke 1–3 and 24 really do group with Acts. The pattern replicates. (Ch. 8, "Marcion, Luke, and Acts")
- Revelation 4–22 really does sit next to Daniel in the Septuagint. (Ch. 8, "Revelation", Exhibit 5)
- Their results that the Pastorals separate from Paul, that Ignatius's 7 authentic letters separate from the 6 forgeries, and that Mark's long ending is later all match mainstream scholarship. (The Pastorals and Mark's ending replicate in this kit; the Ignatius result wasn't tested here.)

---

## 1. Did you test accuracy at chapter length?

> "Your English, Latin and Greek tests used whole novels and whole books. Did you ever test accuracy on 400- to 700-word pieces from authors you already knew?"

**Why it matters:** the book's New Testament results rest on chapters, which they say average about 400 words in Paul and 700 in the Gospels. Their validation tests were never run at that length.

**Where the book says it:**
- Chapter lengths: Ch. 7, "Aren't the texts too small?" (Kindle p. 216): *"Stylo still finds reliable results at the chapter level for the gospels, which is about an average of 700 words. Chapters for the Pauline Epistles… tended to have closer to an average of around 400 words."*
- They nearly didn't run it: same section: *"We almost didn't run our chapter-level analysis due to this concern."*
- Whole-book tests: Ch. 7, "Stylo Demo" (Kindle p. 212): *"Our English, Latin, and Greek tests all had a minimum of 100 texts,"* plus the English novels demo that follows.
- The 96% claim: Ch. 7, "Shouldn't you run x n-grams, x Most Frequent Words, x Delta, etc.?" (Kindle p. 216): they *"not publish an image in this book that uses a method lower than 96% accuracy."*

**What the kit shows:** their own English demo, same novels, same settings:
- whole novels: 95% correct author
- 4,000 words: 60%
- 700 words: 27%
- 400 words: 23% (chance is about 7%)

18 of the 22 novels split into 3–4 different branches at 400 words.

**Show them:** `english_demo/tree_whole` next to `english_demo/tree_400`. The first is our rerun, which matches their figure; the second is the same novels at their chapter length.

**They'll say:** "Our Greek demo got Matthew 5–7 and 1 Timothy 1–3 right." (Ch. 7, the Greek test figure and the paragraph after it, Kindle p. 216)
**You say:** "Those are back-to-back chapters of one passage, compared against classical authors. Across all 28 chapters of Matthew, only 36% match Matthew. Matthew 26 matches Mark 14 and Matthew 27 matches Mark 15." (Step 5 of run_all.)

---

## 2. Which groupings survive Stylo's own consensus test?

> "Stylo has a built-in stability check, the bootstrap consensus tree. Your Final Disclaimer says to make sure a result isn't a fluke of corpus size or settings. Did your key groupings pass it?"

**Where the book says it:** Ch. 7, "Final Disclaimer": *"Make sure it isn't due just to corpus size, or that your n-gram selection isn't appropriate for the size of texts you're running."*

**What the kit shows:** with their settings, only 41% of the chapter-level groupings survive Stylo's 50% consensus rule, only 12% appear in all 10 runs, and 63 chapters have no stable place. (Step 2.)

**They'll say:** "We tested lots of settings."
**You say:** "Then which of your specific groupings, like Luke 1–4 with Acts or Philemon with Colossians, held up across them? The book doesn't show that."

---

## 3. What does a split mean, if single authors split too?

> "Your book treats Acts as one author ('the author of Acts'). With your settings, Acts splits into three branches. Did Acts have three authors? If not, how do you know a split in Paul means different authors?"

**Be careful here:** single authorship of Acts is a strong consensus, not a proven fact, and some scholars think it used earlier sources. The novels (question 1) are your stronger proof, because nobody disputes who wrote them.

**Where the book says it:** Ch. 8, "Marcion, Luke, and Acts": *"If the Gospel of Luke and Acts were written by the same person as tradition claims, then there would likely not be the separation we see here…"* On Paul, Ch. 8, "Summary of the Core Letters of Paul": *"Really, there are only two ways this could have happened."*

**What the kit shows:** Acts splits into chapters 1–12 (Peter, Jerusalem) and 13–28 (Paul's travels), with the trial speeches 22–26 on their own branch. (Step 2, `output/3_acts`.) The novels do the same thing (question 1).

**Follow-up using their own figure:** In Exhibit 7 (Ch. 8, "Mark 13 and the Little Apocalypse"), Acts splits into sub-groups, including 22–26 (the trial speeches) on their own, and the book treats that as one author. In Exhibit 3, Paul splits into sub-groups, and the book treats that as several authors. The distance scale is cropped out of both, so ask: *"What makes one split normal variation and the other a different author?"*

**They'll say:** "Acts may have had multiple authors or sources too."
**You say:** "Fair, so set Acts aside. Your method splits Dickens and Brontë novels the same way at 400 words, and we know exactly who wrote those. At this length, a split is what you get from one author."

---

## 4. How do you rule out genre?

> "You say Stylo identifies the author 'regardless of the topic.' But in your own trees and mine, speeches group with speeches and narrative with narrative. How did you test that genre and type of writing weren't driving your groupings, like the prison letters or Hebrews with Justin?"

**Where the book says it:**
- Ch. 7, "Stylo Demo" (Kindle p. 212): *"regardless of the topic, Stylo correctly identifies the author. It doesn't look at the theme, theology, opinion, topic, or anything like that."* Repeated in Ch. 8, "Revelation."
- Ch. 7, "Could the stylometric analysis be picking up theology, genre, or theme instead of authorship?": *"Genres may come into play at a broader level, but we have tested authors who have letters, historical documents, philosophical pieces, recorded speeches…"*
- **Careful:** in "Paul's Prison Letters" and "The Ignatius Collection Connection," the book uses the shared prison theme as *extra support* for common authorship (*"Given the common theme of the author being in prison, this is not surprising"*). It does **not** say Stylo detected the theme. Don't claim it contradicts itself here.

**What the kit shows:** speech chapters pick another speech chapter as their closest match 63% of the time, against about 20% by chance. Mark 13's closest matches are Matthew 24, Matthew 10, Luke 21 and Luke 12. John 14–16's closest are John 5 and 8, John's other long speeches (step 6). In their own Greek demo, rebuilt, Lucian's narrative *True Story* sits with the historian Appian, and Eusebius's *History* with Josephus (`greek_demo`). Jaaron's scripted and casual videos split apart (`tiktok_test`).

**Be careful with theological words:** θεοῦ, Ἰησοῦς, Χριστοῦ, κυρίου and πνεῦμα are in the top 100 Greek words, which contradicts *"Theological words come way down on the list."* But running with grammar words only gives nearly the same results (52% vs 52–56% same-book matches), so topic words aren't what drives the trees. Genre is: how different kinds of writing use the same common words.

---

## 5. How does resemblance give you a date or a direction?

> "If Luke 1–3 matches Acts, that fits Marcion's gospel coming first. But it also fits one author writing those chapters freely, with Marcion cutting them. What in the stylometry tells you which came first?"

**Where the book says it:** Ch. 8, "Marcion, Luke, and Acts": *"our stylometric analysis definitively proves it."* On dating, Ch. 7, "If stylometric analysis is used to find authorship, how are you using it to find dates?": *"When another letter or document shows up right alongside Ignatius… we can date that document to the second century as well."* The reconstruction they used is named in Ch. 8, "Mark 13 and the Little Apocalypse" (Klinghardt; chapter note 5).

**Why it matters:** stylometry measures similarity. It has no clock and no arrow. Every second-century date in the book comes from the textual arguments, not from the trees.

**Follow-up:** "Reconstructions of Marcion's gospel use Luke's Greek wherever the church fathers are silent. Aren't you partly comparing Luke to Luke?"

---

## 6. The Septuagint test cuts both ways

> "You say Revelation 4–22 was translated from Hebrew because it's close to the Septuagint. But Luke 1–2, which you say the author of Acts wrote in Greek, is just as close to the Septuagint (1.95 vs 1.99), even though it's a much shorter text. If closeness to the Septuagint doesn't mean translation for Luke 1–2, why does it for Revelation?"

**Where the book says it:** Ch. 8, "Revelation" (Exhibit 5): *"Aspects of the original Hebrew being translated come through, indicating that Revelation was originally written in Hebrew…"* Luke 1–2 as the Acts author's own writing: Ch. 8, "Marcion, Luke, and Acts."

**What the kit shows:** step 7. Revelation 4–22's closest match is Daniel, which it alludes to constantly.

**Be careful here:** Luke 1–2's single closest match is Acts, not a Septuagint book, while Revelation's is Daniel. He can point that out. So don't claim the two results are identical. Claim the narrower point: closeness to the Septuagint comes in degrees, a passage written in Greek reaches the same degree, and imitating biblical style explains both. Closeness alone can't show translation.

---

## 7. Will you publish your files?

> "You say none of your data is behind a paywall and anyone can repeat it. Your own Final Disclaimer says the texts included in a run change the branches. So for each Exhibit, which texts were in the run, from which editions, with which settings?"

**What the book does give:** Stylo; "100 MFW, Culled @ 0%, Eder's Simple" on the demo figures; the original Greek; chapter units (about 700 words in the Gospels, 400 in Paul); 2–3 John merged; 1 Clement in 5-chapter blocks; Romans split by Price's divisions; Klinghardt's reconstruction of Marcion's gospel (chapter note 5); Harvey's 1857 Irenaeus.

**What's missing, and what to ask for:**
1. The Greek New Testament edition.
2. The editions of the other hundred-plus texts (Ignatius, Justin, Josephus, 1 Clement and so on).
3. How the Greek was cleaned: accents, punctuation, how words were split.
4. **Which texts were in each Exhibit's run.** This matters most, because of their own warning.
5. The settings for each Exhibit. The Exhibits are cropped without the settings footer, and Ch. 7 says they chose "the most effective way for each language."
6. Uncropped graphs with the distance scale.
7. The full list of segments, including which Pauline chapters were run alone or grouped.
8. Accuracy measured at chapter length.

**Where the book says it:** Ch. 7, "Stylo Demo" (Kindle p. 209): *"None of our data, methodology, or tools are behind paywalls or inaccessible."* Ch. 7, "Final Disclaimer": *"the corpus size - the number of texts you add in - will affect the branches of the graph it creates and the distances between texts."* Ch. 7, "Stylo Demo" (Kindle p. 212): *"we had to crop our results images simply due to the size of the graph."* Ch. 7, "Shouldn't you run x n-grams…": settings chosen as *"the most effective way for each language."*

**Why it matters:** Richard Carrier, himself a mythicist, says the study can't be reproduced as published. The book gives the method but not the inputs.

---

## Factual points, if the conversation turns to the history

- **The coins.** First Revolt coins from year 4 (69–70 CE) read "For the Redemption of Zion." The book's phrase is "Redemption of Israel," so the wording differs, but the slogan's idea was already on coins in 69–70, not only in the 130s. Book: Ch. 8, "Marcion, Luke, and Acts" (Luke 24:9 and Bar Kokhba coins).
- **Polycarp in 2 Timothy.** 2 Timothy 4:13 names Carpus, a different name. Book: Ch. 8, end of "The Irenaeus Irony" and "The Latter Letters."
- **Justin knew Luke 1.** Around 155–160, Justin refers to Gabriel's announcement to Mary in wording close to Luke 1:35 (*Dialogue with Trypho* 100). Most scholars think he used Luke, though he doesn't quote it word for word. The book responds by moving the author from Irenaeus to Polycarp. Book: Ch. 8, end of "The Irenaeus Irony" (*"If there were any genuine, direct quotes from canonical Luke… prior to the time of Irenaeus…"*).
- **The Philemon signature.** Galatians 6:11 and 1 Corinthians 16:21 have the same "in my own hand" line. Book: Ch. 8, "Paul's Prison Letters" (third point, verse 19).
- **Paul before 144.** 1 Clement 47, Polycarp's *Philippians* 3.2 and Ignatius's *Ephesians* 12 all mention Paul's letters. The book redates each one. Book: Ch. 8, "The Finale" and "1 Clement" (*"our first reference to Paul outside the Bible is now into the 130s at the earliest"*).
- **P52.** He's right that it could date as late as about 200 (Nongbri 2005). But that makes it neutral: it fits the book's date and the mainstream one.

---

## Other book claims, with locations

- 2 Thessalonians dated to the 130s (Caligula "too early"): Ch. 8, "The Thessalonian Letters and 2 Corinthians."
- 1 Corinthians "contradictions" and 1:12 "hypocrisy": Ch. 8, "1 Corinthians."
- Romans split by Robert Price's theological divisions: Ch. 8, "Romans."
- John 14–17 a separate author: Ch. 8, "John Documents" (Exhibit 4, about Kindle p. 262).
- Mark 13 dated after 136: Ch. 8, "Mark 13 and the Little Apocalypse" (Exhibit 7).
- Proto-Mark without Mark 13, then dated by its lack of Temple references: Ch. 8, "Reconstructing Proto-Mark," "Less Than Full Marks," and "Marking the Timeline" (Kindle p. 284).
- Irenaeus as author of Luke-Acts (Harvey's 1857 reconstruction, 50+ quotes of Acts): Ch. 8, "The Irenaeus Irony."
- All 15 findings in one list: Ch. 8, "Summarizing Our New Testament Findings" (Kindle p. 276).
- Papias's fragments came out inconclusive, Polycrates "authenticated": Ch. 8, "Papias, Dionysius of Corinth, and Polycrates" (Kindle p. 284).

---

## From their MythVision interview ("Was Jesus Created In The Second Century?", MythVision Podcast)

Their own words, with timestamps. The live Stylo demo runs from about 44:00 to 1:12:00.

| Time | What they say | Why it matters |
|---|---|---|
| 45:24–45:40 | Settings: language "other," words, n-gram 1, cluster analysis, **Eder's Simple**, no sampling, **100 MFW** | The same settings this kit uses |
| 53:07 | *"it's basically the Sermon on the Mount there because that's a pretty coherent unit within Matthew… if you had picked like I don't know the beginning of Matthew and the end of Matthew…"* | They chose an easy, single passage for the demo (question 1) |
| 48:26 | *"because the most frequent words don't get into things outside of filter words it's not being changed by genre or theme"* | The exact claim question 4 tests |
| 59:05 | *"Acts 6 is a really small text… it's always acting weird"* | Acts 6 is 278 words; Paul's chapters have a median of 367, and 9 of 61 are shorter than Acts 6 |
| 38:46 | Philemon *"jumps around a little bit because it's so small"* | They know small texts are unstable |
| 38:15 | *"you run the test over and over again with different things added in or taken away… if things move all around that's… it not getting a very good read"* | The right check. Ask for the results (question 2) |
| 39:01 | *"we only get like 96 to 98% accuracy usually on a run that we are confident in"* | Accuracy on runs they're confident in, not accuracy at a set length |
| 1:05:17 | A 350-word test on three people's group-chat messages | The same easy design as the TikTok demo |
| 34:27 | *"we ran 2200 files… 10 million plus"* | None of it has been published (question 7) |
| 1:11:13 | *"if Paul is a person you could place him there… Romans, second Corinthians, Galatians, First Corinthians"* | Agrees with the whole-book result: the core four look like one author |
| 1:11:45 | *"we see that these still come up with second century text"* | Dating by resemblance (question 5) |

---

## The one-line version

> "Your method works on whole books, and your tests prove that. But at your chapter lengths, it splits Dickens, Acts and Matthew into different 'authors' too. So the splits can't be your evidence, and the dates come from somewhere else."
