#!/usr/bin/env bash
# Runs every test in order. Takes a few minutes.
set -e
cd "$(dirname "$0")"
echo "== 1. Building the chapter files =="
python3 make_corpus.py sblgnt
echo "== 2. Stylo with the authors' settings =="
Rscript run_stylo.R 2>&1 | grep -E "Nearest neighbour|Ac_|^\\$|Done" || true
echo "== 3. Stylo consensus check =="
Rscript consensus_check.R 2>&1 | grep -v "Tk is not available"
echo "== 4. Paul: one voice or a group? =="
python3 paul_test.py
echo "== 5. Noise tests (sample size, 45 settings, shuffled text, Acts, Luke) =="
cd noise_tests
python3 analysis.py > ../output/noise_tests_log.txt
python3 chunk.py > ../output/sample_size.txt
python3 -c "
import json
R = json.load(open('results_simple.json')); C = json.load(open('chunk_simple.json'))
print(f\"Same-book closest match: {R['base_nn_same_book']:.0%} (shuffled text: {R['null_nn_same_book_mean']:.0%})\")
print(f\"Default-tree pairings that hold in 75% of 45 setting combinations: {R['default_pairs_that_survive_75pct']:.0%}\")
print(f\"Chapters whose closest match changes with settings: {R['nn_changes_share']:.0%}\")
for p in C['curve']: print(f\"  {p['size']:>5} words: {p['acc']:.0%} correct\")
"
echo "Done. See the output folder."
