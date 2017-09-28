#!/usr/bin/env python
# ft.py - Find text based on user-supplied keyword or regex
# ft.py kw <keyword> : search for the keyword in files of specific types
# ft.py rg <regex>	 : search for text based on the provided regex
# ft.py type_list 	 : list all types of file to search for
# ft.py type_add  	 : add types of file to search for
# ft.py type_reset	 : reset file type to default
# ft.py setting		 : print current setting
# ft.py igcase 		 : ignore case when searching for text
# ft.py setpath <path> : set searching directory
# ft.py reset  		 : reset setting including file type
# ft.py help

import sys, os, re, glob, shelve

STAR 		= '*'
KEYWORD 	= 'kw'
REGEX 		= 'rg'
LIST 		= 'type_list'
ADD 		= 'type_add'
T_RESET 	= 'reset'
SETTING 	= 'setting'
IGNORE_CASE = 'igcase'
SETPATH 	= 'setpath'
S_RESET 	= 'reset'
C_SENSITIVE = 'sensitive'
C_IGNORED	= 'ignored'
HELP 		= 'help'

# Default file type
init_type = ['.txt']

if __name__ == "__main__":
	# Storing types of files to search 
	fileShelf = shelve.open('fs')
	# Dict of text and their locations
	found_location = {}
	# Init
	if not fileShelf or len(sys.argv) == 2 and sys.argv[1] == S_RESET:
		fileShelf['type'] = init_type
		print type(fileShelf['type'])
		fileShelf['case'] = C_SENSITIVE
		fileShelf['path'] = path = os.getcwd()

	if len(sys.argv) == 2 and sys.argv[1] == HELP:
		print "ft.py kw <keyword>   : search for the keyword in files of specific types\nft.py rg <regex>     : search for text based on the provided regex\nft.py type_list      : list all types of file to search for\nft.py type_add       : add types of file to search for\nft.py type_reset     : reset file type to default\nft.py setting        : print current setting\nft.py igcase 	     : ignore case when searching for text\nft.py setpath <path> : set searching directory\nft.py reset          : reset setting including file type\n"

	elif len(sys.argv) == 2 and sys.argv[1] == LIST:
		print fileShelf['type']

	elif len(sys.argv) == 2 and sys.argv[1] == T_RESET:
		fileShelf['type'] = init_type

	elif len(sys.argv) == 2 and sys.argv[1] == SETTING:
		print fileShelf

	elif len(sys.argv) == 2 and sys.argv[1] == IGNORE_CASE:
		fileShelf['case'] = C_IGNORED

	elif len(sys.argv) == 3 and sys.argv[1] == SETPATH:
		# Check availability of the inputted path before setting
		if os.path.isdir(sys.argv[2]):
			print "Path set!"
			fileShelf['path'] = sys.argv[2]
		else:
			print "Failed setting path!"

	# Adding types of files to search
	elif len(sys.argv) > 2 and sys.argv[1] == ADD:
		for file_type in range(len(sys.argv) - 2):
			temp_list = fileShelf['type']
			type_to_add = sys.argv[file_type + 2]
			# Check duplicate before adding
			if type_to_add not in fileShelf['type']:
				temp_list.append(type_to_add)
				fileShelf['type'] = temp_list

	# Searching using keywords
	elif len(sys.argv) == 3 and sys.argv[1] == KEYWORD:
		for file_type in fileShelf['type']:
			for filename in glob.glob(os.path.join(fileShelf['path'], STAR+file_type)):
				file_to_search = open(filename)
				line_num = 0
				# Search for the keyword in the opened file
				for line in file_to_search:
					line_num += 1
					if sys.argv[2] in line:
						if sys.argv[2] not in found_location:
							found_location[sys.argv[2]] = {filename: [line_num]}
						else:
							found_location[sys.argv[2]][filename].append(line_num)
				file_to_search.close()
		print found_location

	# Search using regex
	elif len(sys.argv) == 3 and sys.argv[1] == REGEX:
		text_regex = re.compile(sys.argv[2])
		for file_type in fileShelf['type']:
			for filename in glob.glob(os.path.join(fileShelf['path'], STAR+file_type)):
				file_to_search = open(filename)
				line_num = 0
				# Search for the keyword in the opened file
				for line in file_to_search:
					line_num += 1
					mo = text_regex.search(line)
					# Found text satisfying regex
					if mo is not None:
						if sys.argv[2] not in found_location:
							found_location[sys.argv[2]] = {filename: [line_num], 'content': [mo.group()]}
						else:
							found_location[sys.argv[2]][filename].append(line_num)
							found_location[sys.argv[2]]['content'].append(mo.group())
				file_to_search.close()
		print found_location

	# Close shelve
	fileShelf.close()



