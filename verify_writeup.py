"""Rerun every script behind the numbers in the public write-up, in reading order, and save all output
to verify_log.txt so you can check each number yourself.

Usage (from the kit folder, in Command Prompt):   py -3.12 verify_writeup.py
Quick mode skips the two slow ones (nt_apply, interp_test):   py -3.12 verify_writeup.py quick
The Ignatius step needs g1.xml and g2.xml in the kit folder (links in TONIGHT_RUNS.md); it is skipped if they're missing.
"""
import os, sys, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
QUICK = "quick" in sys.argv[1:]

# (write-up section, what to look for, command)
STEPS = [
 ("2. The missing number", "400 words / 100 MFW about 63%; 1,500 words about 83%",
  ["advanced/mfw_and_length.py"]),
 ("2. The missing number", "whole novels 95-96%, 4,000 words 60%, 700 words 27%, 400 words 23%",
  ["english_demo/english_demo.py", "english_demo/corpus_whole" if os.path.isdir(os.path.join(HERE, "english_demo", "corpus_whole")) else "100_english_novels/corpus"]),
 ("3. Single authors split too", "Revelation 100%, Acts 89%, Mark 38%, Romans 38%",
  ["advanced/glom_test.py"]),
 ("3. Single authors split too", "Mark 38% -> 88% without Matthew and Luke; Luke 92% (100% without Acts)",
  ["advanced/glom_noparallels.py"]),
 ("3. Single authors split too", "base_nn_same_book 0.52 vs null_nn_same_book_mean 0.10 (shuffled); default_pairs_that_survive_75pct 0.22; nn_changes_share 0.93. (The 41% consensus figure comes from consensus_check.R in RStudio.)",
  ["noise_tests/analysis.py"]),
 ("3 + 4. Ignatius control", "genuine pieces closest to Ignatius 16/20 (80%); genuine vs forged 34/35 (97%) at 400, 13/13 at 1,500",
  ["advanced/ignatius_test.py", "g1.xml", "g2.xml"]),
 ("4. What holds up", "core blocks whose closest block is core Paul 93% (13 of 14); different letter only 64% (9 of 14)",
  ["noise_tests/blind_blocks.py"]),
 ("4. What holds up", "core four with each other 0.97; Acts halves 0.94; Ignatius 0.35; 1 Peter 0.69; James 0.65 (1,500 words)",
  ["advanced/nt_apply.py"]),
 ("5. Grab bag", "contiguous 60% vs grab bag 71% at 400 words",
  ["advanced/sampling_test.py"]),
 ("5. Grab bag", "as is 52%, shuffled 52%, with replacement 49%, 200 words 42%, 100 words 29%, whole book 92%",
  ["advanced/grabbag_chapter.py"]),
 ("6. Dating and direction", "r = 0.18 (p = 0.21); Josephus -> Eusebius 235 years",
  ["advanced/date_vs_style.py"]),
 ("6. Dating and direction", "cut-down Luke: 0.14-0.22 to Luke 4-22 vs 1.40 to Acts, 50 of 50 cuts",
  ["advanced/direction_test.py"]),
 ("6. Dating and direction", "speech chapters pick another speech 63% vs 20% by chance",
  ["book_claims/speech_test.py"]),
 ("Interpolations", "core-letter scores change by 0.07 at most (slow)",
  ["advanced/interp_test.py"]),
]
SLOW = {"advanced/nt_apply.py", "advanced/interp_test.py"}

log = open(os.path.join(HERE, "verify_log.txt"), "w", encoding="utf-8")
def out(s=""):
    print(s); log.write(s + "\n"); log.flush()

out(f"Python: {sys.version.split()[0]}   Started: {time.strftime('%Y-%m-%d %H:%M')}")
for i, (section, expect, cmd) in enumerate(STEPS, 1):
    script = cmd[0]
    out("\n" + "=" * 78)
    out(f"[{i}/{len(STEPS)}] {script}   (write-up: {section})")
    out(f"EXPECT: {expect}")
    out("-" * 78)
    if QUICK and script in SLOW:
        out("skipped in quick mode"); continue
    args = [os.path.join(HERE, c) if c.endswith((".py", ".xml")) or "/" in c else c for c in cmd]
    if any(a.endswith(".xml") and not os.path.exists(a) for a in args):
        out("skipped: g1.xml / g2.xml not found in the kit folder"); continue
    t = time.time()
    r = subprocess.run([PY] + args, cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out((r.stdout or "").rstrip())
    if r.returncode != 0:
        out("ERROR:\n" + (r.stderr or "").strip()[-1500:])
    out(f"({time.time() - t:.0f} s)")
out("\nDone. Compare each EXPECT line with the output under it; everything is saved in verify_log.txt.")
