# Jaaron Wingo's TikTok test, rerun

In his video, Jaaron (Christ Before Jesus) ran 8 transcripts from 4 people through Stylo and called the result "100% accurate" with files as small as 130 words. His settings, from the video: English, words, n-gram 1, 50 most frequent words, culling 0, Eder's Delta, cluster analysis.

This folder reruns that test on public video transcripts:
- `Jaaron_1`, `Jaaron_2`: Jaaron (Christ Before Jesus). `Jaaron_2` is his stylometry demo video.
- `OP_1`: the OP's words quoted at the start of that video.
- `JesusAndWhatnot_1-3`: the Jesus and Whatnot channel.
- `BornAgainAtheist_1-3`: Born Again Atheist.

Run (from this folder):
    python run_tiktok.py     (Windows)   /   python3 run_tiktok.py   (Mac)
    Rscript trees.R          (draws the trees with his exact settings)

Or in Stylo's window: point it at `corpus_his_design` (created by run_tiktok.py) and use his settings above.
To add people, put more transcripts in `texts/` named `Person_1.txt`, `Person_2.txt`, and so on.
