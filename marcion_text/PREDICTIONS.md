# Did Marcion's school write the letters, or edit them? Predictions and rules

Written 2026-10-24, before Part A's search was run and before Book 5 of Tertullian's Against Marcion was read for
coding. Never edited; changes go in AMENDMENTS.md with a date.

## 1. The question

Livesey proposes that Paul's letters were composed c. 144 in Marcion's school, as a collection. The leading recent
Marcion scholars hold instead that Marcion edited letters that already existed:
- Vinzent (2024) cites Galatians 5:21, "as I said before", which he reads as pointing back to 1 Corinthians although
  Marcion's edition put Galatians first;
- Schmid (1995), endorsed by Litwa (2026), argues from pre-Marcionite readings.

Two tests follow.

## 2. Part A: back-references and collection order

**Data:** the ten letters of Marcion's edition, in the SBLGNT: Ro, 1Co, 2Co, Ga, Eph, Php, Col, 1Th, 2Th, Phm.

**Search (backrefs.py):** every passage where a letter refers back to something said, written, taught or handed on
before:
- προλέγω / προεῖπον / προείρηκα ("I said before");
- ἔγραψα, and γράφω with a past or letter reference;
- ἐπιστολή;
- παρήγγειλα / παρηγγείλαμεν, παρέδωκα, ἐδίδαξα / ἐδιδάχθητε, ἐκηρύξαμεν, ἐμάθετε;
- ὑπομιμνῄσκω / ἀναμιμνῄσκω, μνημονεύετε.

**Coding:** each hit is coded by what it points to:
- (i) oral teaching or warning during a visit;
- (ii) an earlier passage of the same letter;
- (iii) an earlier letter to the same addressees;
- (iv) another letter of the collection;
- (v) unclear.

**Test of orders:** for each type (iv) reference, does the letter it points to come earlier in each of these orders?
- Marcion's order (Tertullian, Against Marcion 5): Ga, 1Co, 2Co, Ro, 1Th, 2Th, Eph (as "Laodiceans"), Col, Php, Phm;
- the order by length (the later canonical order): Ro, 1Co, 2Co, Ga, Eph, Php, Col, 1Th, 2Th, Phm;
- P46 (c. 200): Ro, Heb, 1Co, 2Co, Eph, Ga, Php, Col, 1Th.

## 3. Part B: Marcion's own text against Marcion's theology

**Data:** Tertullian, Against Marcion, Book 5 (Latin, Oehler's edition, Perseus canonical-latinLit stoa0275.stoa006).
Tertullian works through Marcion's edition letter by letter. He often argues from what Marcion's own text says.

**Coding:** every passage of Paul that Tertullian quotes or discusses in Book 5 is coded on two axes.
1. **Status in Marcion's text:**
   - **in:** Tertullian says or clearly implies it stood in Marcion's edition (for example "apud Marcionem", "in your
     apostle", or arguing from it against Marcion as from Marcion's own text);
   - **removed/changed:** Tertullian says Marcion deleted or altered it;
   - **unclear.**
2. **Bearing on Marcion's theology.** Marcion's theology is taken in its minimal form, the part Litwa (2025) also
   accepts: the Father of Jesus is not the Creator, the God of Israel and of the law. A passage is:
   - **against on its face:** its own words identify the God or Christ of the letter with the Creator; or present
     Israel's scripture as that God's word and prophecy of Christ; or the law as that God's good law; or Christ as
     coming from Israel according to the flesh;
   - **against only by Tertullian's argument:** Tertullian reads it that way, but a Marcionite reading is natural;
   - **neutral or for Marcion.**

## 4. Decision rules

- **Part A:** if any type (iv) references exist and fit an order other than Marcion's but not Marcion's own, that
  supports Vinzent: Marcion rearranged an earlier collection. If there are none, or all are better read as (i) to
  (iii), Part A cannot decide.
- **Part B:** passages that are "in" Marcion's text and "against on its face" are the test. If a school composed
  these letters to carry Marcion's theology, there should be few or none. Ten or more counts as clear evidence
  against Marcionite composition. Then Livesey's model would need the school to have written, or kept, material
  that refutes its own founder.

## 5. Predictions

1. Most back-references point to oral teaching during a visit (i) or to earlier letters to the same church (iii).
2. Paul's other uses of προλέγω / προεῖπον (1 Thessalonians 3:4; 4:6; 2 Corinthians 13:2) refer to warnings given in
   person. So Galatians 5:21 is most naturally read the same way, and Vinzent's collection-order argument is weak.
3. Part A therefore cannot decide between a collection before Marcion and one made by Marcion's school.
4. Tertullian attributes to Marcion's text at least 15 passages he uses against Marcion.
5. Of those, at least 10 are "against on its face": for example Romans 1:3 has to be checked, and Galatians 4:4
   ("born of a woman, born under the law").
6. Most of Tertullian's arguments are interpretive ("against only by Tertullian's argument").
7. Tertullian reports deletions mainly in Romans (chapters 9-11, 15-16) and Galatians 3.

## 6. Limits stated in advance

- Tertullian is hostile and argues tendentiously. His claims about what Marcion's text contained are the best
  evidence we have, but they are second-hand (Schmid's caution).
- Oehler's 1854 Latin text is old. Where it matters, standard modern editions (Kroymann, Evans) may differ.
- The minimal theology chosen for Marcion is narrower than Tertullian's portrait, so as not to stack the test against
  Livesey.
- Coding is by Claude (an AI model) and needs review.
