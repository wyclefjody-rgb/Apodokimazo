suppressMessages(library(stylo))
for (d in c("corpus_their_demo", "corpus_exhibit6_control")) {
  out <- paste0("tree_", sub("corpus_", "", d)); dir.create(out, showWarnings = FALSE); old <- setwd(out)
  stylo(gui = FALSE, corpus.dir = file.path("..", d), corpus.lang = "Other", analyzed.features = "w", ngram.size = 1,
        mfw.min = 100, mfw.max = 100, culling.min = 0, culling.max = 0, distance.measure = "dist.eder",
        analysis.type = "CA", display.on.screen = FALSE, write.png.file = TRUE, write.pdf.file = FALSE,
        plot.custom.height = 11, plot.custom.width = 8)
  setwd(old)
}
