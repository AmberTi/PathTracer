import string
import re
from collatex import * 
from collections import Counter

"""CLEANING XML FILE: NO TAGS,  NOT DELETIONS (REMOVE DEL TAG AND THE ACTUAL WORDS DELETED)"""

def clean_xml(filename):
	f = open(filename,"r")
	dirty_data = f.read()
	deltag = re.compile(r"<del type=[^>]*>([^<]*?)</del>")
	no_deletion = deltag.sub("", dirty_data) #deleting all deletion tags, and everything in between open & close tag. 

	tags = re.compile(r"<[^>]*>") #deleting (only) tags, remaining: everything in between tags. 
	notags = tags.sub("", no_deletion) #still dirty
	dirt = re.compile(r"(-->)| (&amp;) | (\*\s)+") #erase common dirt (*, &amp symbol, --> arrow)
	data_notags = dirt.sub("", notags)

	punct_list = [",",".","-","!","?",":", "(", ")"] 
	nopunct = [] 
	for character in data_notags: 
		if character in punct_list: 
			character = ""
		else: 
			nopunct.append(character)
	data_notags_nopunct = ("".join(nopunct))

	double_spacing = re.compile(r"\s+ | \n+")
	data_notags_nopunct_nospace = double_spacing.sub(" ", data_notags_nopunct)
	data = data_notags_nopunct_nospace
	return(data)

"""COLLATION"""

collation = Collation()
collation.add_plain_witness("A", clean_xml("Guiltless_49v50.xml"))
collation.add_plain_witness("B", clean_xml("Guiltless_53v54.xml"))
collation.add_plain_witness("C", open("ch7_l30.txt", "r").read())
"""allignment_table = collate(collation, layout='vertical')
print(allignment_table)"""

"""LOW-FREQ WORDSEARCH"""
lowfreqword_list = []
text = clean_xml("Guiltless_49v50.xml").lower().split()
wordcount = Counter(text)
"""print(wordcount)"""

for word in wordcount:
	if wordcount[word] == 1:
		lowfreqword_list.append(word)

"""print(lowfreqword_list)"""

matchwords = []	
for lfword in lowfreqword_list:
	if lfword in clean_xml("Guiltless_53v54.xml").split():#if word in second witness 
		matchwords.append(lfword)

matchword_indices = []
for matchword in matchwords:
	if matchword in clean_xml("Guiltless_53v54.xml").split():
		matchword_indices.append(clean_xml("Guiltless_53v54.xml").split().index(matchword))
"""print(matchword_indices)""" #double checking matchwords
witness_list = clean_xml("Guiltless_53v54.xml").split()
matchsentences = []
for index in matchword_indices:
	matchsentence = list(witness_list[(index-10):(index)]) + list(("<<<").split()) + list(witness_list[index].split()) + list((">>>").split()) + list(witness_list[(index+1):(index+11)])
	matchsentences.append(" ".join(matchsentence))
	print(matchsentences)
for sentence in matchsentences:
	print("Matchword_sequence: ",sentence)













































































































































































































































































































































































































































