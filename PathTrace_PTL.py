import string
import re

f = open("Guiltless_49v50.xml","r")
data = f.read()
tags = re.compile(r"<[^>]*>")
notags = tags.sub("", data) #still dirty
dirt = re.compile(r"(-->)| (&amp;) | (\*\s)+") #erase common dirt
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
print(data_notags_nopunct_nospace)
