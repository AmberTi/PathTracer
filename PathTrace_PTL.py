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

def retrieve_text(file):
	if file.endswith(".xml"):
		text = clean_xml(file)
	else:
		text = open(file, "r").read()
	return text

"""print(retrieve_text("ch7_l30.txt"))"""

def collate_files(fileList):
	alphabet = string.ascii_uppercase #list aplhabet capitalized
	i = 0
	collation = Collation()
	if fileList[1]: #min 2 files in fileList
		for file in fileList:
			if file.endswith(".xml"):
				collation.add_plain_witness(alphabet[i], retrieve_text(file))
			else:
				collation.add_plain_witness(alphabet[i], retrieve_text(file))
			i += 1
		allignment_table = collate(collation, layout='vertical')
		return(allignment_table)
	else:
		raise IOError('At least 2 files needed for collation!')

"""file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
file3 = "ch7_l30.txt"
listOfFiles = [file1, file2, file3]
print(collate_files(listOfFiles))"""

def lowfreq_matchwords(fileList): #finds lowfrequency words from one witness, that occur in complete second witness
	lowfreqword_list = []
	text = retrieve_text(fileList[0]).split()
	wordcount = Counter(text)
	for word in wordcount:
		if wordcount[word] == 1:
			lowfreqword_list.append(word)
	"""print(lowfreqword_list)"""
	
	matchwords = []	
	if fileList[1].endswith(".xml"):
			text = clean_xml(fileList[1]).lower().split()
	else:
		text = open(fileList[1], "r").read().lower().split()
	for lfword in lowfreqword_list:	
		if lfword in text:#if word in second witness 
			matchwords.append(lfword)
	return matchwords

file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
"""print(lowfreq_matchwords([file1, file2]))"""

def print_matchsequences(fileList):
	matchword_indices = []
	matchsequences = []
	i = 0
	for textfile in fileList:
		textfile = retrieve_text(fileList[i]).split()
		for matchword in lowfreq_matchwords(fileList):
			matchword_indices.append(textfile.index(matchword))
		for index in matchword_indices:
			matchsequence = list(textfile[(index-10):(index)]) + list('<') + list(textfile[index].split()) + list('>') +list(textfile[(index+1):(index+11)])
			#matchsequences.append("Sequence matchword in " + fileList[1] + ": " + (" ".join(matchsequence)))
			print("Sequence matchword in " + fileList[i] + ": " + (" ".join(matchsequence)))
		i += 1
 

file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
print_matchsequences([file1, file2])