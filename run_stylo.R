# Re-run of the Christ Before Jesus stylometry in Stylo itself,
# using the settings the authors disclosed by email:
#   100 most frequent words, single words (1-grams), Eder's Simple distance, no culling.
# Run from this folder after make_corpus.py:   Rscript run_stylo.R
suppressMessages(library(stylo))
dir.create("output", showWarnings = FALSE)

their <- list(gui = FALSE, corpus.lang = "Other", analyzed.features = "w", ngram.size = 1,
              mfw.min = 100, mfw.max = 100, culling.min = 0, culling.max = 0,
              distance.measure = "dist.simple", display.on.screen = FALSE,
              write.pdf.file = TRUE, write.png.file = TRUE, plot.custom.height = 40, plot.custom.width = 12)

go <- function(dir, analysis, prefix, ...) {
  work <- file.path("output", prefix); dir.create(work, showWarnings = FALSE)
  old <- setwd(work); on.exit(setwd(old))
  args <- modifyList(their, list(analysis.type = analysis, corpus.dir = file.path("..", "..", dir), ...))
  do.call(stylo, args)
}

# 1. Their setup on all 259 chapters: one cluster-analysis tree
r1 <- go("corpus_nt_chapters", "CA", "1_all_chapters")
d <- as.matrix(r1$distance.table); diag(d) <- Inf
book <- sub("_.*", "", rownames(d))
nn <- apply(d, 1, which.min)
cat(sprintf("Nearest neighbour from the same book: %.0f%%\n", 100 * mean(book == book[nn])))
write.csv(data.frame(chapter = rownames(d), nearest = rownames(d)[nn]),
          "output/1_nearest_neighbours.csv", row.names = FALSE)

# 2. Stylo's own stability check: bootstrap consensus tree, 100 to 1000 words, 50% consensus
go("corpus_nt_chapters", "BCT", "2_consensus", mfw.min = 100, mfw.max = 1000, mfw.incr = 100,
   consensus.strength = 0.5)

# 3. Control: Acts alone (one author by near-universal agreement)
r3 <- go("corpus_acts", "CA", "3_acts", plot.custom.height = 10)
h <- hclust(as.dist(r3$distance.table), method = "ward.D")
print(split(rownames(r3$distance.table), cutree(h, 2)))

# 4. Whole books, their settings
go("corpus_nt_books", "CA", "4_books", plot.custom.height = 10)
cat("Done. Trees (PDF and PNG) and tables are in the output folder, one subfolder per test.\n")
