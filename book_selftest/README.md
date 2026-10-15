# Run their own book through their own method

Their tree of their own chapters sorts the two authors correctly. This checks whether that still holds when
the chapters are cut to the length of a Pauline chapter (400 words), the length the book's Paul conclusions rest on.

1. Save each chapter of your copy of the book as a plain-text file in the `texts` folder, named AUTHOR_CHAPTER.txt:
       Jaaron_01.txt  Jaaron_02.txt  Jaaron_03.txt  Jaaron_06.txt  Jaaron_09.txt  Jaaron_TLDR.txt
       Matthew_04.txt Matthew_05.txt Matthew_07.txt Matthew_08.txt
   (Leave out the Note and Intro unless you know who wrote it.) Copy the text yourself from a copy you own.
   Keep these files private: the book is under copyright, so don't share or upload them anywhere.
2. From this folder:   py -3.12 selftest.py
3. Optional trees in Stylo:   Rscript trees.R

What it prints, for whole chapters and for pieces of 4,000, 1,500, 700 and 400 words (20 random repeats each):
  - how often a piece's closest match is by the same author (from a different chapter, so shared topic can't help)
  - what chance would give
  - how many of the book's own chapters get split across both authors' sides of a 2-group tree
Settings are the book's: 100 most frequent words, culling 0%, Eder's Simple distance, Ward linkage.
