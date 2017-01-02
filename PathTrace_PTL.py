import string
import re
from collatex import * 
from collections import Counter
import os


"""CLEANING XML FILE: NO TAGS,  NOT DELETIONS (REMOVE DEL TAG AND THE ACTUAL WORDS MARKED AS DELETED)"""
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

def collate_files(fileList):
	alphabet = string.ascii_uppercase #list aplhabet capitalized
	i = 0
	collation = Collation()
	if fileList[1]: #min 2 files in fileList
		for file in fileList:
			if file.endswith(".xml"):
				collation.add_plain_witness(alphabet[i], clean_xml(file))
			else:
				collation.add_plain_witness(alphabet[i], open(file, "r").read())
			i += 1
		allignment_table = collate(collation, layout='vertical')
		return(allignment_table)
	else:
		raise IOError('At least 2 files needed for collation!')

file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
file3 = "ch7_l30.txt"
listOfFiles = [file1, file2, file3]
"""collate_files(listOfFiles)"""

def lowfreq_matchwords(file1, file2): #finds lowfrequency words from one witness, that occur in complete second witness
	lowfreqword_list = []
	if file1.endswith(".xml"):
		text = clean_xml(file1).lower().split()
	else:
		text = open(file1, "r").read().lower().split()
	wordcount = Counter(text)
	return wordcount
	
	for word in wordcount:
		if wordcount[word] == 1:
			lowfreqword_list.append(word)
	"""print(lowfreqword_list)"""
	
	matchwords = []	
	for lfword in lowfreqword_list:
		for file in fileList:
			if file2.endswith(".xml"):
				text = clean_xml(file2).lower().split()
			else:
				text = open(file2, "r").read().lower().split()
		if lfword in text:#if word in second witness 
			matchwords.append(lfword)
	return matchwords

file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
print(lowfreq_matchwords(file1, file2))

"""matchword_indices = []
for matchword in matchwords:
	if matchword in clean_xml("Guiltless_53v54.xml").split():
		matchword_indices.append(clean_xml("Guiltless_53v54.xml").split().index(matchword))"""
"""print(matchword_indices)""" #double checking matchwords
"""witnesslist = [clean_xml("Guiltless_49v50.xml").split() , clean_xml("Guiltless_53v54.xml").split()]
matchsentences = []
for witness in witnesslist:
	for index in matchword_indices:
		matchsentence = list(witness[(index-10):(index)]) + list(("<<<").split()) + list(witness[index].split()) + list((">>>").split()) + list(witness[(index+1):(index+11)])
		matchsentences.append(" ".join(matchsentence))"""
"""for sentence in matchsentences:
	print("Sequence matchword in Witness", witnesslist.index(witness)+1 ,sentence)"""












































































































































































































































































































































































































































