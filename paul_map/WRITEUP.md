# What every source says Paul did: the Paul map

Expectations written first: EXPECTATIONS.md (SHA-256 4cdb75db7da7411e74674a8fad6bc8ff308fd49f56f4361bb60452b4c1dbc6ef, never
edited). Data: episodes.txt, sources.txt, events.txt. Generated: MAP.md, paul_map.csv, people.csv (by check_map.py,
which also checks every New Testament reference against the SBLGNT).

## The question

Is there any evidence of Paul outside his own letters, and how well do the sources that tell his story agree?

## What was built

169 reports of 43 episodes in Paul's life, each from one source, sorted into six tiers:
1. the seven undisputed letters (52 reports);
2. the six disputed letters (13);
3. Acts (56);
4. Christian writers to c. 200 (26);
5. legend (8);
6. outside evidence (14).

Each report is classed against the undisputed letters as agreeing, differing (both could be true), conflicting
(both cannot be true as written), absent from the letters, or, for outside evidence, confirming the setting. The
people named with Paul (102) are listed in people.csv.

## Findings

**1. Nothing outside Christian writings names Paul.** The 14 outside reports confirm the world of the story, not
the man:
- Aretas IV's reign;
- Gallio's proconsulship (the Delphi inscription of 52);
- Claudius' expulsion of Jews from Rome;
- the famine of the late 40s;
- the governors Felix and Festus, Drusilla, Agrippa II and Bernice;
- the high priest Ananias;
- the Egyptian prophet;
- the Temple warning notices;
- local titles at Thessalonica, Ephesus and Malta.

Only one of these, Aretas, is in the letters themselves. The rest corroborate Acts. Josephus, who names Felix,
Festus, Ananias, Agrippa and the Egyptian, never mentions Paul, and nor does any Roman writer.

**2. Every other witness to Paul is later than his death.** By the usual dates the earliest is 1 Clement, c. 95;
Acts is c. 80-130. Two silences stand out:
- Papias (c. 110-130), in what survives of him, never mentions Paul.
- Justin Martyr (c. 150-160) never names him, though he lived in Rome when Marcion's edition of Paul was there.

The oldest surviving copy of the letters, P46, is from about 200.

**3. The letters and Acts tell the same outline.** Of the 38 episodes in both, they:
- agree in 14;
- agree where Acts adds something the letters lack in 6;
- differ in 15;
- conflict in 3.

The shared frame runs:
1. a persecutor called near Damascus;
2. a first visit to Jerusalem;
3. Syria and Cilicia;
4. a Jerusalem meeting over circumcision with James and Cephas;
5. churches in Galatia, Macedonia, Achaia and Asia;
6. the same companions;
7. a last journey to Jerusalem;
8. a hope of Rome.

**4. Where they disagree, they disagree on things that matter to Paul.** The three conflicts all concern his
independence from Jerusalem:
- **The first visit.** Galatians swears he saw only Cephas and James; Acts has him moving freely among "the
  apostles".
- **An extra famine visit,** which Galatians' sworn list leaves no room for.
- **The Jerusalem meeting.** In Galatians it is private and "added nothing"; in Acts it is a public council that
  issues a decree Paul never cites, even when he discusses idol food.

There are 15 softer differences. Who chased him at Damascus: Aretas' governor or "the Jews". Whether Timothy was
with him at Athens. How many times he went to Corinth. Whether he was ever in prison before the last arrest. Acts
never says Paul wrote letters, mentions the collection once (24:17), and never names Titus. The letters never call
him Saul, or mention Tarsus, Gamaliel or Roman citizenship.

**5. The later the source, the more it knows.** Each tier adds things the letters lack:
- **Christian writers** add Spain, a joint founding of the churches of Rome and Corinth with Peter, his death in
  Rome, and monuments ("trophies") to the apostles on the Vatican and the Ostian Way. The joint foundings conflict with the letters (Romans is written to a church
  Paul has never visited; in 1 Corinthians, Paul planted and Apollos watered).
- **The legends** add his face (bald, bow-legged, eyebrows meeting), a disciple (Thecla), a baptized lion, and
  milk flowing from his neck at his beheading.

This is the pattern by which legend grows, and the letters show none of it.

## What this means for the corroboration question

By your standard, that an internal detail needs independent corroboration, Paul as a person is attested only by
texts that claim to be his own. Everything outside them is either later, or confirms the setting without naming
him.

The nearest thing to corroboration is where the letters and Acts agree on a detail that neither seems to have taken
from the other. Examples:
- The letters name Crispus as one of the few Paul baptized at Corinth; Acts, without saying so, makes him the
  synagogue ruler who believed.
- Both tell the basket escape from Damascus, but they name different pursuers.
- Prisca and Aquila appear in both; Acts ties their arrival to an expulsion that Suetonius confirms.

William Paley built a whole argument on such "undesigned coincidences" (Horae Paulinae, 1790). Its weakness is that
Acts may have used the letters (Pervo, Dating Acts, 2006). The disagreements count against simple copying, since a
copier would not have contradicted Paul's own oath in Galatians 1:20, but they do not prove independence.

This bears on Livesey only indirectly:
- **The conflicts have no direction by themselves.** Livesey holds that Acts came first and the letters were written
  in Paul's voice afterwards. On that order, the letters' insistence on Paul's independence from Jerusalem (the sworn
  account of the first visit, the private meeting that "added nothing") reads as letters correcting Acts toward
  Marcion's stance. On the usual order, Acts' public council and extra visit read as a later writer smoothing over
  Paul's quarrel with Jerusalem. The map shows the conflicts but cannot say which text answers which; the follow-up
  study acts_order/ tests that.
- **Against an early date,** the map adds nothing new. Outside evidence confirms the 50s setting, but a careful
  later writer could have known it.

## Expectations against outcomes

| expectation (EXPECTATIONS.md section 4) | outcome |
|---|---|
| 1. No outside source names Paul; outside evidence confirms only the setting | yes: 14 reports, none names him |
| 2. Every other Christian source is later than c. 62-67 | yes, by usual dates (the earliest, 1 Clement, c. 95) |
| 3. Letters and Acts share an outline | yes |
| 4. They conflict on the Jerusalem visits, the Damascus pursuers, the first visit, the meeting, Timothy's circumcision, and the Corinth visits | **partly**: the first visit, the famine visit and the meeting were coded "conflicts"; the Damascus pursuers, Timothy's circumcision and the Corinth visits only "differ" (both could be true) |
| 5. Acts never says Paul wrote letters and barely mentions the collection; the letters never mention Saul, Tarsus, Gamaliel or citizenship | yes |
| 6. Later and legendary tiers add details | yes |

## Limits

- Every relation code is a judgment, made by Claude (an AI model), with the reason written in events.txt. It needs a
  person's review, as the Daniel-method checklist did.
- The map lists what the sources say. It does not decide which is right where they differ.
- People are joined by name only, so two men named Gaius count as one, and Acts' Sosthenes is merged with 1
  Corinthians' Sosthenes.
- Dates of the sources are the usual ranges. Livesey dates several of them (the letters, 1 Clement, Ignatius,
  Polycarp) to c. 140-150.
- Outside references were checked against standard editions. Two identifications are flagged as disputed in their
  rows: Sergius Paulus, and Erastus.

## Reproduce

```
python -X utf8 paul_map/check_map.py
```

## Sources

- Delphi (Gallio) inscription: https://en.wikipedia.org/wiki/Delphi_Inscription
- Sergius Paulus inscriptions and the dispute: https://en.wikipedia.org/wiki/Sergius_Paulus
- Muratorian list, text with line numbers: https://bible-researcher.com/muratorian.html
- Publius' title on Malta: https://www.internationalstandardbible.com/P/publius.html
- Aretas IV: https://en.wikipedia.org/wiki/Aretas_IV
- Josephus, Antiquities 20.101 (famine): https://lexundria.com/j_aj/20.101/wst

Research assistance: drafted with Claude (Anthropic).
