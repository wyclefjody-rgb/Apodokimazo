# Draw the trees in Stylo with the settings printed on the book's figure.
suppressMessages(library(stylo))
for (d in c("corpus_whole", "corpus_400")) {
  out <- paste0("tree_", sub("corpus_", "", d)); dir.create(out, showWarnings = FALSE)
  old <- setwd(out)
  stylo(gui = FALSE, corpus.dir = file.path("..", d), mfw.min = 100, mfw.max = 100, culling.min = 0, culling.max = 0,
        distance.measure = "dist.simple", analysis.type = "CA", display.on.screen = FALSE,
        write.png.file = TRUE, write.pdf.file = FALSE, plot.custom.height = ifelse(d == "corpus_whole", 8, 22), plot.custom.width = 9)
  setwd(old)
}
