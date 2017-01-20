import string
import re
from collatex import * 
from collections import Counter
import os
from operator import itemgetter

def cls(): 
	"""Emptying screen: as found on https://mail.python.org/pipermail/tutor/2013-May/095252.html & http://stackoverflow.com/questions/517970/how-to-clear-python-interpreter-console"""
	os.system('cls' if os.name=='nt' else 'clear')

def clean_xml(filename):
	"""Retrieve text from an .xml (as used at UA): taking out all the tags and frequently occuring 'dirt' as well as all words marked by a deletion-tag."""
	f = open(filename,"r", encoding='utf-8')
	dirty_data = f.read()
	uncleartag = re.compile(r"(<unclear>)|(</unclear>)") #unclear tag often occurs within del tags have to take out first, otherwise still in final text.
	dirty_data_noUnclear = uncleartag.sub(" ", dirty_data)
	deltag = re.compile(r"<del type=[^>]*>([^<]*?)</del>")
	no_deletion = deltag.sub("", dirty_data_noUnclear) #deleting all deletion tags, and everything in between open & close deletion-tag. 
	tags = re.compile(r"<[^>]*>") #deleting all (only) tags remaining. What's left after this is everything in between tags, = text.
	notags = tags.sub("", no_deletion)
	dirt = re.compile(r"(-->)| (&amp;) | (\*\s)+ | (\n)* | (\s)*") #erase common dirt (*, &amp symbol, --> arrow and (double) spacing)
	data_notags = dirt.sub(" ", notags)

	punct_list = [",",".","-","!","?",":", "(", ")"] 
	bracketdash = ["(" , "-"] #apart: characters with no whitespace àfter
	punct_split = [] 
	for character in data_notags: 
		if character in punct_list: 
			punct_split.append(" " + character)
		elif character in bracketdash:
			punct.split.append(character + " ")
		else: 
			punct_split.append(character)

	data_notags_punctsplit = ("".join(punct_split)) #in this text string punctuation is preceded and followed by whitespace
	double_spacing = re.compile(r"\s+ | \n+") #delete doublespacing
	data_notags_punctsplit_nospace = double_spacing.sub(" ", data_notags_punctsplit)
	data = data_notags_punctsplit_nospace #renaming 
	return(data)

def retrieve_text(file):
	"""Make textstring of ttxt/xml file, depends on the file that is given."""  
	if file.endswith(".xml"): 
		text = clean_xml(file)
	else: #if .txt
		text_punct = open(file, "r").read() 
		punct_list = [",",".","-","!","?",":", ")"] #//.xml in retrieve_text module. To prevent missing a match because of 'sticky' punctuation. 
		bracketdash = ["(" , "-"]  
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
	"""Using CollateX, collating two or more text strings (retrieved from files) with previous modules. 
	Returns a grid with corresponding words/sequences next to each other"""
	#i = 0
	collation = Collation() #add off function name to new variable
	if fileList[1]: #min 2 files in fileList 
		for file in fileList:
			collation.add_plain_witness(file, retrieve_text(file)) #add witness (textstring) to Collation()
		allignment_table = collate(collation, layout='vertical')
		return(allignment_table)
	else:
		raise IOError('At least 2 files needed for collation!')

def sorted_frequencies (fileList):
	"""Frequency dictionary of all words in text strings, retrieved from files in fileList. If more files are given, all words in text strings are brought together.
	Returns a frequency dictionary , sorted by value (highest value at top)."""
	freq_dict_list = []
	text = []
	for file in fileList:
		currentText = retrieve_text(file).split() #split string into words (list of strings)
		for word in currentText: 
			if word not in [",",".","-","!","?",":", "(", ")"]:
				text.append(word)
	freq_dict = Counter(text)
	for w in sorted(freq_dict, key=freq_dict.get, reverse=True): # as found on : stackoverflow.com/questions/16375404/how-do-i-find-the-most-common-words-in-multiple-separate-texts
		freq_dict_list.append("".join(str(w) + " : " + str(freq_dict[w]))) 
	return freq_dict_list

def lowfreq_words(file):
	"""Puts all words with a given 'wordcount[word]=' frequency in list."""
	lowfreqword_list = []
	text = retrieve_text(file).split()
	wordcount = Counter(text)
	for word in wordcount:
		if wordcount[word] == 1:
			if word not in [",",".","-","!","?",":", "(", ")"]: #make sure that no punctuation ends up in the lowfrequency-words list. Should not be problem so long as freq = 1, but if higher might be. 
				lowfreqword_list.append(word)
	return lowfreqword_list

def lowfreq_matchwords (fileList):
	"""This module searches for the lowfrequency words (from the module above) in a second and third witness. 
	CAUTION! order matters : if fileList = [f1, f2, f3], then f1 = file from which lowfrequency words are retrieved , f2 = second witness , f3 = third witness""" 
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
		for word in match2ndfile: #is low frequency word from first file in 2nd ànd 3rd file.
			if word in (retrieve_text(fileList[2]).split()):
				matchwords.append(word)
	return (matchwords)

def print_matchsequences(fileList):
	"""Returns for each witness (text string retrieved from file in fileList) the "sequence" (+/- sentence) in which the lowfrequency matchword (lowfreq_matchword) occurs.
	the fileList can consist of either 2 or 3 files. Result: (depending on #files) 2 or 3 sequences, each of occurrence of matchword in f1, f2 (and f3).
	CAUTION! Order matters.""" 
	matchsequences = [] #The list in which "sequences" of both files will be stored.
	prettysequences = []
	matchwords = lowfreq_matchwords(fileList)
	for file in fileList:
		text = retrieve_text(file).split()
		matchword_indices = [] #emptying the list (especially needed after the first iteration)
		for matchword in matchwords:
			matchword_indices.append(text.index(matchword))
		
		currMatchsequence = [] #list for the matchsequences of the current file, emptying needed after first iteration
		x = 10 
		for index in matchword_indices:
			if index < x:
				limiter = x #limiter = word around which the sequence will be built.
			elif index+x >= len(text):
				limiter = len(text)-(x+1)
			else:
				limiter = index
			currMatchsequence.append(file + " : " +" ".join(text[(limiter-x):index]) + " << " + text[index] + " >> " + " ".join(text[index+1:(limiter+x)]))
		matchsequences.append(currMatchsequence) #after 2 ir 3 iterations, will contain 2 or 3 (#files) lists with the matchsequences of both files. List of lists.

	i = 0
	for seq in matchsequences[0]: #only iterate as many times as there are values in the first list (= amount of matchwords)
		if len(fileList) == 3:
			prettysequences.append((matchsequences[0][i] + "\n" + matchsequences[1][i] + "\n" + matchsequences[2][i] + "\n\n")) #using indexing to address each string in matchsequences. 
			i += 1
		else: #if len == 2
			prettysequences.append((matchsequences[0][i] + "\n" + matchsequences[1][i] + "\n\n")) 
			i += 1
	return prettysequences

def find_word_in_files (input_word, fileList):
	"""Find a given 'input_word' in different files (or, strings retrieved from...) in fileList. Return for each file: file, index and occurrence-sequence of input_word"""
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
				x = 20 #variable, easy to adjust. 
				if index < x:
					limiter = x #upper or lower limit. If index < x, limiter has to become x (because then, after subtraction of x, limiter == 0): 0 as lower limit.
				elif index+x >= len(text): #if index + x > len, error will occur (our of range), so: upper limit = len(text) - x+1 (because index != len)
					limiter = len(text)-(x+1) 
				else:
					limiter = index
				input_word_sequence = (" ".join(text[(limiter-x):index]) + " << " + text[index] + " >> " + " ".join(text[index+1:(limiter+x)]))
				found.append("Found it! It's in " + file + " under index \"" + str(index) + "\" in the following sequence : " + input_word_sequence)
			index += 1
		if not foundInCurrentFile:
				notfound.append("Sorry, I couldn't find the word(s) \"" + str(input_word) + "\" in the following file: " + file)
	if not foundInAnyFile:
		nowhere.append("Sorry, I couldn't find the word(s) in any of the files.")
	return(found, notfound, nowhere) 

def ReOccuringDeletions(fileList): 
	"""fileList consist of 2 files. 
	With file1 being an .xml and the file you take the deletions from and file 2 being the file you want to check on deletions re-occurrences.""" 
	if len(fileList) == 2:

		f = open(fileList[0] , "rt")
		text = f.read()
		textf2 = retrieve_text(fileList[1]).split()

		deletions = []
		lengthyDeletions = []
		returningDelword = []
		delSequences = []
		delword_indices = []
		currMatchsequence = []
		matchsequences = []
		deletionsreoccuring = []
		givenlength = 8 # = minimum length of deleted word. Easier to adjust when in variable

		amp = re.compile(r"&amp;")
		noamp = amp.sub(" " , text)
		deltag_regex = re.compile(r">\n*\s*([^>]*?\s*)\n*\s*\t*<del type=[^>]*>([^<]*?)</del>\n*\s*\t*<[^>]*>\n*\s*\t*([^<]*?)\n*\s*\t*<") #retrieving all text before, in between, after deltag. 
		deletions = deltag_regex.findall(noamp) #forms list of (mini)tuples
		for tup in deletions:
			for string in tup:
				"".join(string.split()) #list of tuples, each consisting of 3 strings 

		for tup in deletions:
			deleted = tup[1] #text that got deleted (text in between del-tag)
			wordsInString = deleted.split() #split for exact match. Otherwise: e.g. "an" will match on "and"
			for item in wordsInString:
				if len(item) >= givenlength:
					lengthyDeletions.append(item)
		
		for tup in deletions:
			for word in lengthyDeletions:
				if word in tup[1].split():
					delSeq = "".join(word + " --> " + tup[0] + " << " +  tup[1] + " >> " +  tup[2]) #highlight part that has been deleted (!= just the word)
					delSequences.append(delSeq) #"pretty" sequence of deletion. 
		
		for word in lengthyDeletions:
			if word in textf2: #if the longer, deleted words in file1 occur in file2, this means that the deleted word has a second occurrence.
				returningDelword.append(word)
		for delword in returningDelword:
			delword_indices.append(textf2.index(delword))
		x = 15 
		for index in delword_indices:
			if index < x:
				limiter = x
			elif index+x >= len(textf2):
				limiter = len(textf2)-(x+1)
			else:
				limiter = index
			currMatchsequence.append(textf2[index] + " --> " + " ".join(textf2[(limiter-x):index]) + " << " + textf2[index] + " >> " + " ".join(textf2[index+1:(limiter+x)]))
		matchsequences.append(currMatchsequence) 
		
		for string in delSequences:
			string = string.split()
			for lst in matchsequences: 
				for seqitem in lst:
					seqitem = seqitem.split()
					if seqitem[0] == string[0]:
						deletionsreoccuring.append("Deleted word & sequence in " + fileList[0] + " : "+ " ".join(string))
						deletionsreoccuring.append("Re-occurrence & sequence in " + fileList[1] + " : "+ " ".join(seqitem) + "\n\n")
					else: #if not equal (if not match), continue.
						pass
	else: 
		raise IOError('At least 2 files needed for collation!')
	return deletionsreoccuring


"""ALL MODULES FOR MAINMENU START HERE (As found on : https://www.youtube.com/watch?v=kGY9n5H6nr0)"""

def showCurrentDir():
	"""Shows all current files in directory of the program"""
	i = 1 #to easily select files
	fileSelector = [] #list to contain all the local directory's files
	for file in os.listdir(os.curdir): #returns list of files in current directory. 
		print(i, file)
		fileSelector.append(file)
		i += 1
	print("") #crete space between files in directory and input ">"
	return(fileSelector)

def filePicker(AmountFiles):
	"""Given the amount of files (a module can take) and which files, this module will select the asked-for files and put them in a list"""
	if not AmountFiles == 0:
		print("\nChoose", AmountFiles, "files:\n") 
		fileSelector = showCurrentDir() #give files (in directory) from which to choose 

		fileList = []
		while len(fileList) < AmountFiles: #number of files cannot be equal/larger than AmountFiles
			item = input("> ") #in this case input = number. 
			fileList.append(fileSelector[int(item)-1]) #file1 has index 0

		print(fileList)
		return(fileList)

	else: #if amount of files == 0 ("eternal" amount of files)
		print("\nChoose as many files as you'd like and end with a return:")
		fileSelector = showCurrentDir()

		fileList = []
		item = input("> ") #for first iteration
		while item: #as long as it's not empty, repeat.
			fileList.append(fileSelector[int(item)-1])
			item = input("> ")

		print(fileList)
		return(fileList)

def menuFunctions(choice):
	"""This module holds all the different modules/functions created above, and returns the module that's been chosen for (input number)."""
	cls() #empty command prompt/screen

	if choice == 1: #segment comparison
		print("Collate text in two or more files (.xml or .txt) using CollateX.")
		fileList = filePicker(0) #0 because no specific amount of files needed.
		print(collate_files(fileList))
		f = open('files/collate_collateX.txt', 'wt')
		f.write(str(collate_files(fileList)))
		print("I have saved this table for you in a file called \"collate_collateX.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()

	elif choice == 2: #low freq comparison
		print("Collate meaningful (low-frequency) words in 1st file with (entire) 2nd (and 3rd) file.")
		print("\nCAUTION! Order matters : \n\tfirst file chosen is the file from which lowfrequency words are retrieved. \n\tthese lowfrequency words will be searched for in second and third chosen file.")
		fileList = filePicker(0)
		for prettyseq in print_matchsequences(fileList):
			print(prettyseq)
		f = open('files/collate_meaningful.txt', 'wt')
		for seq in print_matchsequences(fileList):
			f.write((seq + "\n\n"))
		print("\nI have saved these text fragments for you in a file called \"collate_meaningful.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()

	elif choice == 3:
		print("Find given word in given file(s).")
		f = open('files/given_word.txt', 'wt')
		input_word = input("Enter word you're looking for: ")
		fileList = filePicker(0)
		for lst in find_word_in_files (input_word, fileList):
			for line in lst:
				print(line)
				f.write(str(line)+ "\n")
		print("\nI have saved the occurences of the word" "\"" , input_word,  "\"" "in a file called \"given_word.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()

	elif choice == 4:
		print("Give frequencies of all words (together) in given files.")
		fileList = filePicker(0) #if you pick multiple files, this function takes the frequency of the words of the # files together. 
		f = open('files/sorted_frequencies.txt', 'wt')
		f.write("Sorted frequencies in " + str(fileList) + " : " + "\n")
		for item in sorted_frequencies(fileList):
			print(item)
			f.write((item + "\n"))
		print("\nI have saved the sorted frequencies of the words in " + str(fileList) + " in a file called \"sorted_frequencies.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()
		
	elif choice == 5:
		print("Retrieve text from input file(s). (presumably .xml)")
		fileList = filePicker(0)
		f = open('files/retrieved_text.txt', 'wt')
		for file in fileList:
			f.write("".join("Text from " + (file) + " : \n" + retrieve_text(file) + "\n\n"))
			print(("Text from " + (file) + " : \n" + retrieve_text(file) + "\n\n"))
		print("\nI have saved the retrieved text(s) in " + str(fileList) + " in a file called \"retrieved.text.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()

	elif choice == 6:
		print("Re-occurring deletions: search for words that have been deleted. Do they reappear somewhere else?")
		print("\nCAUTION! the first file you pick must be one with an .xml extension. The second file can be anything.")
		fileList = filePicker(2)
		f = open('files/reoccuring_deletions.txt', 'wt')
		print("The re-occurrence of deletions in file " + str(fileList[0]) + " in " + str(fileList[1]) + ":\n")
		f.write("The re-occurrence of deletions in file " + str(fileList[0]) + " in " + str(fileList[1]) + ":\n")
		for item in ReOccuringDeletions(fileList):
			print(item)
			f.write((str(item) + "\n"))
		print("\nI have saved the re-occurrence of deletions in " + str(fileList[0]) + " in " + str(fileList[1]) +  "in a file called \"reoccuring_deletions.txt\" in the folder \"files\" in the directory of this program. You're welcome!")
		f.close()
		
def mainMenu(errorMessage):
    cls()
    print("Hi! This is Amber's program\n\nPlease choose the function you would like to run:\n 1. COLLATE text in two or more files (.xml or .txt) using CollateX. \n\tOutput: grid with word-on-word collation of text.\n 2. COLLATE MEANINGFUL (low-frequency) WORDS in 1st file with (entire) 2nd (and 3rd) file . \n\tOutput: text fragments of occurence of meaningful words in all two/three files (& index)\n 3. FIND GIVEN WORD in given file(s). \n\tOutput: file, index and text fragment where given word occurs.\n 4. Give FREQUENCIES of all words (together) in given files. \n\tOutput: sorted frequencies. \n 5. RETRIEVE TEXT from input file(s). (presumably .xml) \n\tOutput: 'cleaned' text (aka the text the rest of the program works with). \n 6. RE-OCCURRING DELETIONS: search for words that have been deleted. Do they reappear somewhere else? \n\tOutput: deletion-sequence & corresponding re-occurrence-sequence")
   
    if errorMessage: #if error, show error. 
        print(errorMessage)
        
    menu_answer = input("> ")
    menu_answer_int = int(menu_answer) 
    
    if menu_answer_int == 1:
        menuFunctions(1) #if number is given, this number will be used as input to select function/module.
    elif menu_answer_int == 2:
        menuFunctions(2)
    elif menu_answer_int == 3:
        menuFunctions(3)
    elif menu_answer_int == 4:
    	menuFunctions(4)
    elif menu_answer_int == 5:
    	menuFunctions(5)
    elif menu_answer_int == 6:
    	menuFunctions(6)
    else:
    	mainMenu("This function does not exist (yet)! Try again.")

    returnToMenu()
    
def returnToMenu():
	input("\nPress return when you want to return to the main menu.")
	mainMenu("Welcome back.")
	
mainMenu("")
