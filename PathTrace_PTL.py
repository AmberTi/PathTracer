import string
import re
from collatex import * 
from collections import Counter
import os
from operator import itemgetter

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

def retrieve_text(file): #make text string of text/xml file 
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

def sorted_frequencies (fileList): #frequencydict of all files in fileList
	freq_dict_list = []
	text = []
	for file in fileList:
		currentText = retrieve_text(file).split()
		text += currentText

	#sorting and displaying the words by frequency http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
	sorted_freq_list = sorted(Counter(text).items(), key=itemgetter(1), reverse=True)

	for item in sorted_freq_list:
		print(str(item[0]) + " : " + str(item[1]))

file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
fileList = [file1, file2]

def lowfreq_words(file):
	lowfreqword_list = []
	text = retrieve_text(file).split()
	wordcount = Counter(text)
	for word in wordcount:
		if wordcount[word] == 1:
			lowfreqword_list.append(word)
	return lowfreqword_list

#print(lowfreq_words(file1))

"""def lowfreq_words(fileList): #finds lowfrequency words from THE FIRST witness, that occur in complete second witness
	lowfreqword_list = []
	for file in fileList:
		
	freq_dict_fileList = freq_dict(fileList)
	for word in freq_dict_fileList[0][1]:
		if freq_dict_fileList[0][1][word] == 1:
			lowfreqword_list.append(word)
	lowfreq_words = set(lowfreqword_list)
	return lowfreq_words"""



def lowfreq_matchwords (fileList): #are lowfreqwords from witness 1 in witness 2 ? 
	lowfreqwords = lowfreq_words(fileList[0])

	matchwords = []	
	text = retrieve_text(fileList[1]).split()
	for lfword in lowfreqwords:	
		if lfword in text: 
			matchwords.append(lfword)
	return matchwords

file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
fileList = [file1, file2]
#print(lowfreq_matchwords(fileList))

def match_indices(fileList): 
	matchwords = lowfreq_matchwords(fileList)
	matchword_indices = []
	i = 0
	for matchword in matchwords:
			matchword_indices.append([matchword, [[fileList[i], (retrieve_text(fileList[i]).split()).index(matchword)],[fileList[i+1], (retrieve_text(fileList[i+1]).split()).index(matchword)]]])
	return matchword_indices
#print(match_indices(fileList))
	
def match_sequences(fileList):
	matchsequences = []
	matchword_indices = match_indices(fileList)
	for match in matchword_indices:
		#print(match[0]) #corresponds with first element of eacht matchy-thingy
		"""file1 = match[1][0][0] #name file -> also in fileList, same order
								file2 = match[1][1][0] #name file"""
		index_file1 = match[1][0][1]
		index_file2 = match[1][1][1]
		#print(index_file1, index_file2)

	i = -1
	for match in matchword_indices:
		for file in fileList:
			i += 1
		index = match[1][i][1]
		matchsequence = list((retrieve_text(file).split())[index-10:index]) + list('<') + list((retrieve_text(file).split())[index]) + list('>') + list((retrieve_text(file).split())[(index+1):(index+11)])
		print(matchsequence)
		matchsequences.append(" ".join(matchsequence))
		#"Sequence matchword in " + fileList[1] + ": " + (" ".join(matchsequence))
		print("MATCHSEQUENCE " , matchsequences)


#print for each witness the "sentence" in which the matchword (lowfreq_matchword) occurs. Result: for each matchword 2 sequences.
def print_matchsequences(fileList):
	matchsequences = [] #The list in which we will be placing the "sentences" of both files
	matchwords = lowfreq_matchwords(fileList)
	for file in fileList:
		text = retrieve_text(file).split()
		matchword_indices = [] #emptying the list (especially needed after the first iteration)
		for matchword in matchwords:
			matchword_indices.append(text.index(matchword))
		
		#limiter = het woord waarrond we de zin willen bouwen (bv 5 woorden voor en na de limiter tonen)
		currMatchsequence = [] #list for the matchsequences of the current file, emptying needed after first iteration
		for index in matchword_indices:
			if index < 5:
				limiter = 5
			elif index+6 >= len(text):
				limiter = len(text)-7
			else:
				limiter = index
			currMatchsequence.append(" ".join(text[(limiter-5):index]) + " < " + text[index] + " > " + " ".join(text[index+1:(limiter+6)]))
		matchsequences.append(currMatchsequence) #after 2 iterations, this list will contain 2 lists with the matchsequences of both files.
	#print(matchsequences)

	i = 0
	for seq in matchsequences[0]: #only iterate as many times as there are values in the first list (=amount of matchwords)
		print(matchsequences[0][i] + " | " + matchsequences[1][i])
		i += 1


	'''for index in matchword_indices:
								if index < 10:
									index = 0
								elif index+10 > len(text):
									index = len(text)-1'''
		#print(index)
		#matchsequence = list(text[(index-10):(index)]) + list('<') + list(text[index].split()) + list('>') +list(text[(index+1):(index+11)])
		#(not needed) matchsequences.append("Sequence matchword in " + fileList[1] + ": " + (" ".join(matchsequence)))
		#print("Sequence matchword in " + file + ": " + (" ".join(matchsequence)))
print_matchsequences(fileList)
		
""" file in fileList:
i += 1
index = match[1][i][1]
matchsequence = list((retrieve_text(file).split())[index-10:index]) + list('<') + list((retrieve_text(file).split())[index]) + list('>') + list((retrieve_text(file).split())[(index+1):(index+11)])
print(matchsequence)
print("_________________________________________________________")
matchsequences.append(" ".join(matchsequence))
#"Sequence matchword in " + fileList[1] + ": " + (" ".join(matchsequence))
print("MATCHSEQUENCE " , matchsequences)"""

"""for lst in matchword_indices:
			index = lst[1]
			if index-10 < 0:
				index = 0
			elif index+10 > len(textfile):
				index = len(textfile)-1
			matchsequence = list(textfile[(index-10):(index)]) + list('<') + list(textfile[index].split()) + list('>') +list(textfile[(index+1):(index+11)])
			matchsequences.append("Sequence matchword in " + fileList[1] + ": " + (" ".join(matchsequence)))
		for matchseq in matchsequences:
			print(matchseq)
			i += 1"""

file1 = "Guiltless_49v50.xml"
file2 = "ch7_l30.txt"
fileList = [file1, file2]
#print(match_sequences(fileList))


def index_matchword_dict (fileList):
	i = 0
	dict_idx_matchword_w1 = {}
	dict_idx_matchword_w2 = {}
	dict_list = [dict_idx_matchword_w1, dict_idx_matchword_w2]
	matchwords = lowfreq_matchwords(fileList)
	for file in fileList:
		for matchword in matchwords:
			#matchword_index = (retrieve_text(file).index(matchword)) 
			dict_list[i][retrieve_text(file).index(matchword)] = matchword
		i += 1
			#matchword_dict[matchword_indices.append(textfile.index(matchword))] = matchword
	#return("index & corresp matchword in ", fileList[0], dict_list[0] , "index & corresp matchword in ", fileList[1], dict_list[1])
	return dict_list


file1 = "Guiltless_49v50.xml"
file2 = "Guiltless_53v54.xml"
fileList = [file1, file2]



"""[list(fileList[i][(start_seqindex):(key)]) + list('<') + list(fileList[i][key].split()) + list('>') +list(fileList[i][(key+1):(key+11)])]"""