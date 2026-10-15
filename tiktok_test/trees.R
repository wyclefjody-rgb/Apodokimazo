# His settings from the video: English, words, n-gram 1, MFW 50, culling 0, Eder's Delta, cluster analysis
suppressMessages(library(stylo))
for (d in c("corpus_as_sent", "corpus_his_design")) {
  out <- paste0("tree_", sub("corpus_", "", d)); dir.create(out, showWarnings = FALSE); old <- setwd(out)
  stylo(gui = FALSE, corpus.dir = file.path("..", d), corpus.lang = "English", analyzed.features = "w", ngram.size = 1,
        mfw.min = 50, mfw.max = 50, culling.min = 0, culling.max = 0, distance.measure = "dist.eder",
        analysis.type = "CA", display.on.screen = FALSE, write.png.file = TRUE, write.pdf.file = FALSE,
        plot.custom.height = 6, plot.custom.width = 8)
  setwd(old)
}
