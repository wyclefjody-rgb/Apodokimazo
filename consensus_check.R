# Stylo's bootstrap consensus procedure, done step by step so we can COUNT what survives.
# Same recipe Stylo's BCT uses: a Ward tree at 100, 200, ... 1000 most frequent words,
# then keep only the groupings that appear in at least half of those trees.
# Run after run_stylo.R:   Rscript consensus_check.R
suppressMessages({library(stylo); library(ape)})
freqs <- read.table("output/1_all_chapters/table_with_frequencies.txt", check.names = FALSE)
freqs <- t(freqs)                      # rows = chapters, columns = words (ordered by frequency)
trees <- list()
for (m in seq(100, 1000, 100)) {
  d <- dist.simple(freqs[, 1:m])
  trees[[as.character(m)]] <- as.phylo(hclust(d, method = "ward.D"))
}
cons <- consensus(trees, p = 0.5)
n <- nrow(freqs)
full_tree_groups <- n - 2                       # internal groupings in a fully resolved tree
kept <- cons$Nnode - 1
root_kids <- sum(cons$edge[, 1] == n + 1 & cons$edge[, 2] <= n)
default_groups <- prop.clades(trees[["100"]], trees)   # how many runs contain each grouping of the 100-word tree
cat(sprintf("Groupings in the 100-word tree: %d\n", full_tree_groups))
cat(sprintf("Groupings that survive in >=50%% of runs: %d (%.0f%%)\n", kept, 100 * kept / full_tree_groups))
cat(sprintf("Groupings of the 100-word tree found in ALL 10 runs: %d (%.0f%%)\n",
            sum(default_groups[-1] == 10), 100 * mean(default_groups[-1] == 10)))
cat(sprintf("Chapters left loose at the root of the consensus tree: %d\n", root_kids))
pdf("output/2_consensus/consensus_tree_counted.pdf", width = 12, height = 40)
plot(cons, cex = .5, main = "Consensus of 10 Stylo runs (100-1000 words), 50% rule")
invisible(dev.off())
png("output/2_consensus/consensus_tree_counted.png", width = 1200, height = 4000, res = 100)
plot(cons, cex = .5, main = "Consensus of 10 Stylo runs (100-1000 words), 50% rule")
invisible(dev.off())
