import string
import re
from collatex import * 
from collections import Counter
import os
from operator import itemgetter

#lijn 2-4 = scherm leegmaken/opkuisen. de functie cls() kan overal oproepen worden om het scherm opnieuw leeg te maken, 
#handig om een rommelig scherm te vermijden. helpt met indruk van een GUI te geven

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

"""CLEANING XML FILE: NO TAGS,  NOT DELETIONS (REMOVE DEL TAG AND THE ACTUAL WORDS MARKED AS DELETED)"""
def clean_xml(filename):
	f = open(filename,"r", encoding='utf-8')
	dirty_data = f.read()
	deltag = re.compile(r"<del type=[^>]*>([^<]*?)</del>")
	no_deletion = deltag.sub("", dirty_data) #deleting all deletion tags, and everything in between open & close tag. 
	tags = re.compile(r"<[^>]*>") #deleting (only) tags, remaining: everything in between tags. 
	notags = tags.sub("", no_deletion) #still dirty
	dirt = re.compile(r"(-->)| (&amp;) | (\*\s)+") #erase common dirt (*, &amp symbol, --> arrow)
	data_notags = dirt.sub(" ", notags)

	punct_list = [",",".","-","!","?",":", "(", ")"]
	bracketdash = ["(" , "-"] 
	punct_split = [] 
	for character in data_notags: 
		if character in punct_list: 
			punct_split.append(" " + character)
		elif character in bracketdash:
			punct.split.append(character + " ")
		else: 
			punct_split.append(character)
	data_notags_punctsplit = ("".join(punct_split))

	double_spacing = re.compile(r"\s+ | \n+")
	data_notags_punctsplit_nospace = double_spacing.sub(" ", data_notags_punctsplit)
	data = data_notags_punctsplit_nospace
	return(data)

def retrieve_text(file): #make text string of text/xml file 
	if file.endswith(".xml"):
		text = clean_xml(file)
	else:
		text_punct = open(file, "r", encoding='utf-8').read()
		punct_list = [",",".","-","!","?",":", ")"] 
		bracketdash = ["(" , "-"] #only character with no space after. 
		punct_split = [] 
		for character in text_punct: 
			if character in punct_list: 
				punct_split.append(" " + character)
			elif character in bracketdash:
				punct_split.append(character + " ")
			else:
				punct_split.append(character)
		text = ("".join(punct_split))
	return text

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

def sorted_frequencies (fileList): #frequencydict of all files in fileList
	freq_dict_list = []
	text = []
	for file in fileList:
		currentText = retrieve_text(file).split()
		for word in currentText: 
			if word not in [",",".","-","!","?",":", "(", ")"]:
				text.append(word)
	freq_dict = Counter(text)
	for w in sorted(freq_dict, key=freq_dict.get, reverse=True):
		freq_dict_list.append("".join(w + " : " + str(freq_dict[w]) + "\n"))
	return freq_dict_list

def lowfreq_words(file):
	lowfreqword_list = []
	text = retrieve_text(file).split()
	wordcount = Counter(text)
	for word in wordcount:
		if wordcount[word] == 1:
			if word not in [",",".","-","!","?",":", "(", ")"]: #make sure that no punctuation ends up in the lowfrequency-words list. Should not be problem so long as freq = 1, but if higher might be. 
				lowfreqword_list.append(word)
	return lowfreqword_list

def lowfreq_matchwords (fileList): #are lowfreqwords from witness 1 in witness 2 and 3 : ORDER MATTERS!!
	matchwords_return = []
	lowfreqwords=  lowfreq_words(fileList[0])
	matchwords = []
	if len(fileList) == 2:
		text = (retrieve_text(fileList[(1)]).split())
		for lfword in lowfreqwords:	
			if lfword in text: 
				matchwords.append(lfword)
	elif len(fileList) == 3:
		match2ndfile = []
		text = (retrieve_text(fileList[1]).split())
		for lfword in lowfreqwords:	
			if lfword in text: 
				match2ndfile.append(lfword)
		for word in match2ndfile:
			if word in (retrieve_text(fileList[2]).split()):
				matchwords.append(word)
	return (matchwords)

#print for each witness the "sentence" in which the matchword (lowfreq_matchword) occurs. Result: for each matchword 2 sequences.

def print_matchsequences(fileList):
	matchsequences = [] #The list in which we will be placing the "sentences" of both files
	prettysequences = []
	matchwords = lowfreq_matchwords(fileList)
	for file in fileList:
		text = retrieve_text(file).split()
		matchword_indices = [] #emptying the list (especially needed after the first iteration)
		for matchword in matchwords:
			matchword_indices.append(text.index(matchword))
		
		#limiter = het woord waarrond we de zin willen bouwen (bv 5 woorden voor en na de limiter tonen)
		currMatchsequence = [] #list for the matchsequences of the current file, emptying needed after first iteration
		for index in matchword_indices:
			if index < 10:
				limiter = 10
			elif index+10 >= len(text):
				limiter = len(text)-11
			else:
				limiter = index
			currMatchsequence.append(" ".join(text[(limiter-10):index]) + " < " + text[index] + " > " + " ".join(text[index+1:(limiter+10)]))
		matchsequences.append(currMatchsequence) #after 2 iterations, this list will contain 2 lists with the matchsequences of both files.
	#print(matchsequences)
	i = 0
	for seq in matchsequences[0]: #only iterate as many times as there are values in the first list (=amount of matchwords)
		if len(fileList) == 3: #if there are 3 files in the filelist
			prettysequences.append((matchsequences[0][i] + "\n" + matchsequences[1][i] + "\n" + matchsequences[2][i] + "\n\n")) 
			i += 1
		else:
			prettysequences.append((matchsequences[0][i] + "\n" + matchsequences[1][i] + "\n\n")) 
			i += 1
	return prettysequences

def find_word_in_files (input_word, fileList):
	foundInAnyFile = False #when at least 1 word has been found in ANY file, this will be set to true
	found = []
	notfound = []
	nowhere = []
	for file in fileList:
		foundInCurrentFile = False #when at least 1 word has been found in THE CURRENT file, this will be set to true
		text = retrieve_text(file).split() #split because if string, might match on half words etc.
		index = 0 #to get the index of the current word
		for word in text:
			if word == input_word:
				foundInAnyFile = True
				foundInCurrentFile = True
				x = 20 #made a variable, easy to adjust. 
				if index < x:
					limiter = x
				elif index+x >= len(text):
					limiter = len(text)-(x+1)
				else:
					limiter = index
				input_word_sequence = (" ".join(text[(limiter-x):index]) + " < " + text[index] + " > " + " ".join(text[index+1:(limiter+x)]))
				found.append("Found it! It's in" + file + "under index \"" + str(index) + "\" in the following sequence :" + input_word_sequence)
			index += 1
		if not foundInCurrentFile:
		#I used + (concatenation) instead of , here so there wouldn't be any spaces around the input_word
				notfound.append("Sorry, I couldn't find the word(s) \"" + str(input_word) + "\" in the following file: " + file)
	if not foundInAnyFile:
		nowhere.append("Sorry, I couldn't find the word(s) in any of the files.")
	return(found, notfound, nowhere)

#function for doing something with del/add tags 
"""<del type=[^>]*>([^<]*?)</del>
<add type=[^>]*>([^<]*?)</add>"""

#main menu functions below this line

def showCurrentDir():
	i = 1 #to easily select files
	fileSelector = [] #list to contain all the local directory's files
	for file in os.listdir(os.curdir): #returns list of files in current directory
		print(i, file)
		fileSelector.append(file)
		i += 1
	print("")
	return(fileSelector)

def filePicker(maxFiles):
	if not maxFiles == 0:
		print("Choose", maxFiles, "files:\n")
		fileSelector = showCurrentDir()

		fileList = []
		while len(fileList) < maxFiles:
			item = input("> ")
			fileList.append(fileSelector[int(item)-1])

		print(fileList)
		return(fileList)

	else:
		print("Choose as many files as you'd like and end with a return:")
		fileSelector = showCurrentDir()

		fileList = []
		item = input("> ") #for first iteration
		while item: #as long as it's not empty, repeat.
			fileList.append(fileSelector[int(item)-1])
			item = input("> ")

		print(fileList)
		return(fileList)


def menuFunctions(choice):
	cls()

	if choice == 1: #segment comparison
		print("Collate text in two or more files (.xml or .txt) using CollateX.")
		fileList = filePicker(0) #0 because no specific amount of files needed.
		print(collate_files(fileList))
		print("I have saved this table for you in a file called \"collate_collateX.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f = open('files/collate_collateX.txt', 'wt', encoding='utf-8')
		f.write(str(collate_files(fileList)))
		f.close()

	elif choice == 2: #low freq comparison
		print("Collate meaningful (low-frequency) words in 1st file with (entire) 2nd file.")
		fileList = filePicker(0)
		for prettyseq in print_matchsequences(fileList):
			print(prettyseq)
		print("\nI have saved these text fragments for you in a file called \"collate_meaningful.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f = open('files/collate_meaningful.txt', 'wt', encoding='utf-8')
		for seq in print_matchsequences(fileList):
			f.write((seq + "\n\n"))
		f.close()

# http://stackoverflow.com/questions/27261392/returning-every-element-from-a-list-python
	elif choice == 3:
		print("Find given word in given file(s).")
		f = open('files/word_occur.txt', 'wt', encoding='utf-8')
		input_word = input("Enter word you're looking for: ")
		fileList = filePicker(0)
		for lst in find_word_in_files (input_word, fileList):
			for line in lst:
				print(line)
				f.write(str(line)+ "\n")
		print("\nI have saved the occurences of the word" "\"" , input_word,  "\"" "in a file called \"word_occur.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()

	elif choice == 4:
		print("Give frequencies of all words (together) in given files.")
		fileList = filePicker(0) #if you pick multiple files, this function takes the frequency of the words of the # files together. 
		f = open('files/sorted_frequencies.txt', 'wt')
		for item in sorted_frequencies(fileList):
			f.write(str(item))
		print("\nI have saved the sorted frequencies of the words in " + str(fileList) + " in a file called \"sorted_frequencies.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()
		for value in sorted_frequencies(fileList):
			print(value)

def mainMenu(errorMessage):
    cls()
    print("Hi! This is Amber's program\n\nPlease choose the function you would like to run:\n 1. Collate text in two or more files (.xml or .txt) using CollateX. \n\tOutput: grid with word-on-word collation of text.\n 2. Collate meaningful (low-frequency) words in 1st file with (entire) 2nd file. \n\tOutput: text fragments of occurence of meaningful words in both files (& index)\n 3. Find given word in given file(s). \n\tOutput: file, index and text fragment where given word occurs.\n 4. Give frequencies of all words (together) in given files. \n\tOutput: sorted frequencies")
    
    #als er een errormessage wordt meegegeven aan de functie wordt deze getoond.
    if errorMessage:
        print(errorMessage)
        
    #hier eventueel nog validatie insteken zodat je enkel nummers kan ingeven en geen letters
    menu_answer = input("> ")
    menu_answer = int(menu_answer)
    
    if menu_answer == 1:
        menuFunctions(1)
    elif menu_answer == 2:
        menuFunctions(2)
    elif menu_answer == 3:
        menuFunctions(3)
    elif menu_answer == 4:
    	menuFunctions(4)
    else:
        mainMenu("This function does not exist (yet)! Try again.")

    returnToMenu()
    
def returnToMenu():
	input("\nPress return when you want to return to the main menu.")
	mainMenu("Welcome back.")
	
mainMenu("")