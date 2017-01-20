## TextComparison: a program for manuscript & text comparison.

### Introduction

The program "TextComparison" has been developed in the context of a course on "Programming for Linguistics" in the Master studies on Digital Text Analysis at the University of Antwerp. 
This program can be used to compare different text-editions, or, more specifically, two manuscript versions. The University of Antwerp accommodates two centres for text genetics. For digitizing manuscripts (and their variety of aspects), these centres use a complex .xml structure. The .xml structures of the digitized manuscripts allow to run all sorts of tests on these manuscripts. Due to copyrights, I cannot append the digitized manuscript to the repository. 
"TextComparison" consists of 6 modules of tests that can be runned on two or more versions of one manuscript (or text).  


### Modules/function

The program offers 6 modules/functions:

1
COLLATE text in two or more files (.xml or .txt) using CollateX. 
Output: grid with word-on-word collation of text.

Using the CollateX dictionary (http://collatex.net/doc/) this module collates two or more text strings (retrieved from files given). The module returns a grid with corresponding words/sequences next to each other.


2 
COLLATE MEANINGFUL (low-frequency) WORDS in 1st file with (entire) 2nd file. 
Output: text fragments of occurence of meaningful words in both files (& index)

This module searches for the lowfrequency words from a given (fist) file in a second and third file. Caution: order matters!
Output: wordsequences (+/- sentences) of eahc occurrence of the lowfrequency word in the two or three given files.


3 
FIND GIVEN WORD in given file(s). Output: file, index and text fragment where given word occurs.

This module finds a given 'input_word' in different files (or, strings retrieved from...) in fileList. Return for each file: file, index and occurrence-sequence of input_word.
	

4 
Give FREQUENCIES of all words (together) in given files. Output: sorted frequencies.

This module makes a frequency dictionary of all words in text strings, retrieved from files in fileList. If more files are given, all words in text strings are brought together. Returns a frequency dictionary , sorted by value (highest value at top).


5
RETRIEVE TEXT from input file(s). (presumably .xml) Output: 'cleaned' text (aka the text the rest of the program works with).
This module retrieves text from an .xml (as used at UA): taking out all the tags and frequently occuring 'dirt' as well as all words marked by a deletion-tag.
	

6 
RE-OCCURRING DELETIONS: search for words that have been deleted. Do they reappear somewhere else? Output: deletion-sequence & corresponding re-occurrence-sequence

This module searches for words that have been deleted in an earlier version of a text, that re-occur in a subsequent version (after all). This module takes two files: with file1 being an .xml and the file you take the deletions from and file 2 being the file you want to check on deletions re-occurrences.


### Used Libraries
- string
- re
- collatex
- collections
- os
- operator


### How to.. 

This program runs locally. Even though it has the look & feel of a GUI, you can simply run it via your command prompt.
The results of the modules/tests/functions will be saved automatically in the directory of the program. 
