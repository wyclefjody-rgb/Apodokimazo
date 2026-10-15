# Trees in Stylo with the book's settings: whole chapters, then 400-word pieces
suppressMessages(library(stylo))
for (d in c("corpus_whole", "corpus_400")) {
  if (!dir.exists(d)) next
  out <- paste0("tree_", sub("corpus_", "", d)); dir.create(out, showWarnings = FALSE); old <- setwd(out)
  stylo(gui = FALSE, corpus.dir = file.path("..", d), corpus.lang = "English", analyzed.features = "w", ngram.size = 1,
        mfw.min = 100, mfw.max = 100, culling.min = 0, culling.max = 0, distance.measure = "dist.simple",
        analysis.type = "CA", display.on.screen = FALSE, write.png.file = TRUE, write.pdf.file = FALSE,
        plot.custom.height = ifelse(d == "corpus_whole", 7, 14), plot.custom.width = 8)
  setwd(old)
}
cat("Trees saved in tree_whole and tree_400\n")
