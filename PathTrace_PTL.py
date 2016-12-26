import string
import re

f = open("Guiltless_49v50.xml","r")
data = f.read()
tags = re.compile(r"<[^>]*>")
notags = tags.sub("", data) #still dirty
dirt = re.compile(r"(-->)| (&amp;) | (xx+) | *\s+") #erase common dirt
notags_clean = dirt.sub("", notags)
clean_data = " ".join(notags_clean.split()) #erase double spacing 
"""print(type(clean_data)) """


punct_list = [",",".","-","!","?",":"] 
clean_data_nopunct = [] 
for character in clean_data: 
	if character in punct_list: 
		character = ""
	else: 
		clean_data_nopunct.append(character)
print("".join(clean_data_nopunct))
