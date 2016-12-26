import string
import re
from collatex import * 

def clean_xml(filename):
	f = open(filename,"r")
	dirty_data = f.read()
	tags = re.compile(r"<[^>]*>")
	notags = tags.sub("", dirty_data) #still dirty
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

"""print(clean_xml("Guiltless_49v50.xml"))"""


"""COLLATION"""
collation = Collation() # tell the collation library to create a new instance by saying Collation()
collation.add_plain_witness("A", clean_xml("Guiltless_49v50.xml"))
collation.add_plain_witness("B", clean_xml("Guiltless_53v54.xml"))
alignment_table = collate(collation, layout='vertical')
print( alignment_table)