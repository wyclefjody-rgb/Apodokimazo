"""
    The Paul map: checks the hand-built tables and summarizes them.

    Reads (all in this folder):
      episodes.txt   id | episode | when | where
      sources.txt    source | tier | usual date | notes
      events.txt     episode | source | reference | people | relation | what it says

    Checks:
      - every row names a known episode, a known source and an allowed relation (EXPECTATIONS.md section 3);
      - undisputed letters are always "letters", outside evidence always "setting", and nothing else is either;
      - every New Testament reference (MorphGNT book codes, e.g. "Ga 1:18-20; 2Co 11:32-33") exists in the SBLGNT,
        and belongs to the book the row's source names.

    Writes:
      paul_map.csv   one row per report, with the episode and source details joined in
      people.csv     everyone named with Paul: episodes, sources and tiers
      MAP.md         per-episode attestation, letters against Acts, outside corroboration, people

    Usage (from the kit folder):   python -X utf8 paul_map/check_map.py
"""
import csv
import os
import re
import sys
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..")
SBLGNT = os.path.join(KIT, "sblgnt")
EPISODES = os.path.join(HERE, "episodes.txt")
SOURCES = os.path.join(HERE, "sources.txt")
EVENTS = os.path.join(HERE, "events.txt")
OUTPUT_CSV = os.path.join(HERE, "paul_map.csv")
PEOPLE_CSV = os.path.join(HERE, "people.csv")
OUTPUT_MD = os.path.join(HERE, "MAP.md")

RELATIONS = ["letters", "agrees", "differs", "conflicts", "not in letters", "setting"]
TIER_NAMES = {"1": "undisputed letters", "2": "disputed letters", "3": "Acts", "4": "Christian writers to c. 200",
              "5": "legend", "6": "outside evidence"}
BOOKS = {"Romans": "Ro", "1 Corinthians": "1Co", "2 Corinthians": "2Co", "Galatians": "Ga", "Philippians": "Php",
         "1 Thessalonians": "1Th", "Philemon": "Phm", "2 Thessalonians": "2Th", "Colossians": "Col",
         "Ephesians": "Eph", "1 Timothy": "1Ti", "2 Timothy": "2Ti", "Titus": "Tit", "Acts": "Ac", "2 Peter": "2Pe"}
GROUPS = {"Undisputed letters": {"Ro", "1Co", "2Co", "Ga", "Php", "1Th", "Phm"},
          "Disputed letters": {"2Th", "Col", "Eph", "1Ti", "2Ti", "Tit"}}
ALIASES = {"Peter": "Cephas / Peter", "Cephas": "Cephas / Peter", "Silas": "Silas / Silvanus",
           "Silvanus": "Silas / Silvanus", "Priscilla": "Prisca / Priscilla", "Prisca": "Prisca / Priscilla",
           "Mark": "John Mark", "Sopater": "Sopater / Sosipater", "Sosipater": "Sopater / Sosipater"}
REFERENCE = re.compile(r"^(?:(\d?[A-Z][a-z]+) )?(?:(\d+):)?(\d+)(?:-(?:(\d+):)?(\d+))?$")


def read_rows(path, width):
    rows = []
    with open(path, encoding="utf8") as file:
        number = 0
        for line in file:
            number += 1
            if line.startswith("#") or not line.strip():
                continue
            cells = re.split(r"\s+\|\s+", line.rstrip("\n"), maxsplit=width - 1)
            if len(cells) != width:
                sys.exit(f"{os.path.basename(path)} line {number}: expected {width} columns, found {len(cells)}")
            rows.append((number, cells))
    return rows


def known_verses():
    verses = set()
    for book in set(BOOKS.values()):
        paths = glob(os.path.join(SBLGNT, f"*-{book}-morphgnt.txt"))
        if not paths:
            sys.exit(f"No MorphGNT file for {book} in '{SBLGNT}'. Run setup_data.py first.")
        with open(paths[0], encoding="utf8") as file:
            for line in file:
                code = line.split()[0]
                verses.add((book, int(code[2:4]), int(code[4:6])))
    return verses


def parse_references(text):
    """Returns (book, chapter, verse) for every verse named as a start or end point, or None if text has no
    New Testament reference. Raises ValueError on a reference it cannot read."""
    found = []
    book = None
    chapter = None
    for group in text.split(";"):
        for part in group.split(","):
            part = part.strip()
            match = REFERENCE.match(part)
            if not match:
                if found or part.split(" ")[0] in set(BOOKS.values()):
                    raise ValueError(part)
                return None
            if match.group(1):
                book = match.group(1)
                if book not in set(BOOKS.values()):
                    if found:
                        raise ValueError(part)
                    return None
            if book is None:
                return None
            if match.group(2):
                chapter = int(match.group(2))
            elif match.group(1):
                raise ValueError(part)
            found.append((book, chapter, int(match.group(3))))
            if match.group(5):
                if match.group(4):
                    chapter = int(match.group(4))
                found.append((book, chapter, int(match.group(5))))
    return found


def person(name):
    return ALIASES.get(name, name)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    episodes = {}
    order = []
    for number, (code, title, when, where) in read_rows(EPISODES, 4):
        episodes[code] = (title, when, where)
        order.append(code)
    sources = {}
    for number, (name, tier, date, notes) in read_rows(SOURCES, 4):
        sources[name] = (tier, date)
    verses = known_verses()
    problems = []
    events = []
    for number, (code, source, reference, people, relation, says) in read_rows(EVENTS, 6):
        where = f"events.txt line {number}"
        if code not in episodes:
            problems.append(f"{where}: unknown episode {code}")
            continue
        if source not in sources:
            problems.append(f"{where}: unknown source '{source}'")
            continue
        if relation not in RELATIONS:
            problems.append(f"{where}: unknown relation '{relation}'")
        tier = sources[source][0]
        if (tier == "1") != (relation == "letters"):
            problems.append(f"{where}: tier {tier} with relation '{relation}'")
        if (tier == "6") != (relation == "setting"):
            problems.append(f"{where}: tier {tier} with relation '{relation}'")
        try:
            points = parse_references(reference)
        except ValueError as error:
            problems.append(f"{where}: cannot read reference '{error}'")
            points = None
        if source in BOOKS or source in GROUPS:
            if points is None:
                problems.append(f"{where}: {source} row without a New Testament reference")
                points = []
            allowed = GROUPS.get(source, {BOOKS.get(source)})
            for book, chapter, verse in points:
                if (book, chapter, verse) not in verses:
                    problems.append(f"{where}: {book} {chapter}:{verse} is not in the SBLGNT")
                if book not in allowed:
                    problems.append(f"{where}: {book} cited in a row whose source is {source}")
        names = []
        if people != "-":
            for name in people.split(", "):
                names.append(name.strip())
        events.append({"episode": code, "source": source, "tier": tier, "reference": reference, "people": names,
                       "relation": relation, "says": says})
    if problems:
        print("\n".join(problems))
        sys.exit(f"{len(problems)} problems; nothing written.")

    with open(OUTPUT_CSV, "w", encoding="utf8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["episode", "episode title", "when (conventional)", "where", "source", "tier", "tier name",
                         "source date", "reference", "people", "relation to the letters", "what it says"])
        for event in events:
            title, when, where = episodes[event["episode"]]
            writer.writerow([event["episode"], title, when, where, event["source"], event["tier"],
                             TIER_NAMES[event["tier"]], sources[event["source"]][1], event["reference"],
                             ", ".join(event["people"]), event["relation"], event["says"]])

    by_episode = {}
    for code in order:
        by_episode[code] = []
    for event in events:
        by_episode[event["episode"]].append(event)

    lines = ["# The Paul map", "",
             "Generated by check_map.py from episodes.txt, sources.txt and events.txt. Rules: EXPECTATIONS.md. "
             f"{len(events)} reports in {len(order)} episodes; every New Testament reference checked against the "
             "SBLGNT.", "",
             "## Reports by tier and relation to the undisputed letters", ""]
    header = "| tier |"
    rule = "|---|"
    for relation in RELATIONS:
        header += f" {relation} |"
        rule += "---|"
    lines.append(header + " total |")
    lines.append(rule + "---|")
    for tier in sorted(TIER_NAMES):
        row = f"| {tier} {TIER_NAMES[tier]} |"
        total = 0
        for relation in RELATIONS:
            count = 0
            for event in events:
                if event["tier"] == tier and event["relation"] == relation:
                    count += 1
            total += count
            row += f" {count} |"
        lines.append(row + f" {total} |")
    lines.append("")

    lines.append("## Each episode: who reports it, and how Acts compares with the letters")
    lines.append("")
    lines.append("Tiers: 1 undisputed letters, 2 disputed letters, 3 Acts, 4 Christian writers to c. 200, 5 legend, "
                 "6 outside evidence (confirms the setting, never names Paul).")
    lines.append("")
    lines.append("| episode | when | tiers | letters vs Acts | outside evidence |")
    lines.append("|---|---|---|---|---|")
    standing = {}
    for code in order:
        title, when, where = episodes[code]
        tiers = []
        acts = []
        outside = []
        for event in by_episode[code]:
            if event["tier"] not in tiers:
                tiers.append(event["tier"])
            if event["tier"] == "3":
                if event["relation"] not in acts:
                    acts.append(event["relation"])
            if event["tier"] == "6" and event["source"] not in outside:
                outside.append(event["source"])
        tiers.sort()
        in_letters = "1" in tiers
        if in_letters and acts:
            if "conflicts" in acts:
                verdict = "conflict"
            elif "differs" in acts:
                verdict = "differ"
            elif "agrees" in acts:
                verdict = "agree"
            else:
                verdict = "Acts adds"
        elif in_letters:
            verdict = "letters only"
        elif acts:
            verdict = "Acts only"
        else:
            verdict = "later sources only"
        standing[code] = verdict
        shown = "; ".join(outside) if outside else "-"
        lines.append(f"| {code} {title} | {when} | {' '.join(tiers)} | {verdict} | {shown} |")
    lines.append("")
    lines.append("| letters vs Acts | episodes |")
    lines.append("|---|---|")
    for verdict in ["agree", "Acts adds", "differ", "conflict", "letters only", "Acts only", "later sources only"]:
        codes = []
        for code in order:
            if standing[code] == verdict:
                codes.append(code)
        lines.append(f"| {verdict} | {len(codes)}: {', '.join(codes) if codes else '-'} |")
    lines.append("")
    lines.append("\"Acts adds\": the letters have the episode and Acts reports only things the letters do not. An "
                 "episode counts as a conflict if any Acts report in it conflicts with the letters, so one episode "
                 "can hold agreeing and conflicting details.")
    lines.append("")

    lines.append("## Conflicts and differences, in full")
    lines.append("")
    for relation in ["conflicts", "differs"]:
        lines.append(f"### {relation}")
        lines.append("")
        for event in events:
            if event["relation"] == relation:
                lines.append(f"- **{event['episode']} {episodes[event['episode']][0]}** ({event['source']}, "
                             f"{event['reference']}): {event['says']}")
        lines.append("")

    lines.append("## Outside evidence")
    lines.append("")
    lines.append("None of these names Paul. Each confirms a person, office or event that a Paul story uses.")
    lines.append("")
    for event in events:
        if event["tier"] == "6":
            lines.append(f"- **{event['episode']} {episodes[event['episode']][0]}** ({event['source']}, "
                         f"{event['reference']}): {event['says']}")
    lines.append("")

    people = {}
    for event in events:
        for name in event["people"]:
            key = person(name)
            if key not in people:
                people[key] = {"episodes": [], "sources": [], "tiers": []}
            entry = people[key]
            if event["episode"] not in entry["episodes"]:
                entry["episodes"].append(event["episode"])
            if event["source"] not in entry["sources"]:
                entry["sources"].append(event["source"])
            if event["tier"] not in entry["tiers"]:
                entry["tiers"].append(event["tier"])
    ranked = []
    for key in people:
        entry = people[key]
        entry["tiers"].sort()
        ranked.append((-len(entry["episodes"]), -len(entry["tiers"]), key))
    ranked.sort()
    with open(PEOPLE_CSV, "w", encoding="utf8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["person", "episodes", "number of episodes", "tiers", "in undisputed letters", "in Acts",
                         "sources"])
        for count, spread, key in ranked:
            entry = people[key]
            writer.writerow([key, " ".join(entry["episodes"]), len(entry["episodes"]), " ".join(entry["tiers"]),
                             "yes" if "1" in entry["tiers"] else "no", "yes" if "3" in entry["tiers"] else "no",
                             "; ".join(entry["sources"])])

    both = []
    letters_only = []
    acts_only = []
    for count, spread, key in ranked:
        tiers = people[key]["tiers"]
        if "1" in tiers and "3" in tiers:
            both.append(key)
        elif "1" in tiers:
            letters_only.append(key)
        elif "3" in tiers:
            acts_only.append(key)
    lines.append("## People around Paul")
    lines.append("")
    lines.append(f"{len(people)} people are named with Paul (aliases joined: Cephas/Peter, Silas/Silvanus, "
                 "Prisca/Priscilla). People are joined by name only, so two men called Gaius or Sosthenes count as one. "
                 "Full list: people.csv.")
    lines.append("")
    lines.append(f"- **In both the undisputed letters and Acts ({len(both)}):** {', '.join(both)}")
    lines.append(f"- **Undisputed letters, not Acts ({len(letters_only)}):** {', '.join(letters_only)}")
    lines.append(f"- **Acts, not the undisputed letters ({len(acts_only)}):** {', '.join(acts_only)}")
    lines.append("")
    lines.append("| person | episodes | tiers |")
    lines.append("|---|---|---|")
    for count, spread, key in ranked:
        if -count >= 3:
            lines.append(f"| {key} | {' '.join(people[key]['episodes'])} | {' '.join(people[key]['tiers'])} |")
    lines.append("")

    with open(OUTPUT_MD, "w", encoding="utf8") as file:
        file.write("\n".join(lines) + "\n")
    print(f"All checks passed: {len(events)} reports, {len(order)} episodes, {len(people)} people.")
    print(f"Wrote {OUTPUT_MD}, {OUTPUT_CSV}, {PEOPLE_CSV}")


if __name__ == "__main__":
    main()
