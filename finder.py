#!/usr/bin/python2
# Copyright (C) 2015 OCEAN collaboration
#
# This file is part of the OCEAN project and distributed under the terms 
# of the University of Illinois/NCSA Open Source License. See the file 
# `License' in the root directory of the present distribution.
#
#Melanie Zito. July 2017

import shutil, os, sys

commona = open("Common/pp.dir", "r")
searcha = commona.readlines()
commona.close()

for index, line in enumerate(searcha):
        dir_string = index, line
        print "\nList of everything found in znucl file (in Common):"
        print dir_string[1]
        dir_asked_for = dir_string[1].split()
        for dir in dir_asked_for:
                absolute_path = dir
#search pp.dir in Common to get the absolute path, a will use this



#znucl code:

a = os.path.join(absolute_path)
aalist = os.listdir(a)
alist = sorted(aalist)
numa = map(int, alist)
#lists everything in pseudo directory    

commonz = open("Common/znucl", "r")
searchz = commonz.readlines()
commonz.close()

#looks at znucl file in Common


print "Available elements (by atomic number):"
print alist

element_names = {
        1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 
        10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K",
        20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
        30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y",
        40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "Zr",
        50: "Sn", 51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr",
        60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm",
        70: "Yb", 71: "Lu", 72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au",
        80: "Hg", 81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac",
        90: "Th", 91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es",
        100: "Fm", 101: "Md", 102: "No", 103: "Lr"
}
#list of atomic numbers with their corresponding symbol

for number in numa:
	if number in element_names:
		print "Atomic number " + str(number) + " is " + element_names[number] 
	else:
		print "Name has not been inputed yet for atomic number " + str(number)
#for each of the znucl options listed. if the atomic number is in element_names, print the element name, else, say it's not there





#An attempt to shorten stuff:

def print_once(statement):
	statement_list = []
	if statement not in statement_list:
		statement_list.append(statement)
		print statement
#should print each thing it's called on only once


        


#the final pathmaking code:

def pathmaker1():
	startdict = {}
	lastdict = {}

	#print "pathmaker1"

	for object in zdict:
		start = os.path.join(a, zdict[object])
		#print start #get rid of this later
		startdict[object] = start
	return startdict

def pathmaker2():
	nextdict = {}
	semicore = semicore_list()
	print "\nSemicore dictionary:"
	print semicore	
		
	#print "in pathmaker2"
	for object in pathmaker1():
		next = os.path.join(pathmaker1()[object], semicore[object])
		#print next #get rid of this later
		nextdict[object] = next
	return nextdict	

def pathmaker3():
        lastdict = {}
	qual = quality_list()
	
	pathlist = []
	for object in pathmaker2():
		last = os.path.join(pathmaker2()[object], qual[object])
		#print last #get rid of this later
		lastdict[object] = last		

		pathlist.append(last)
		#need to grab the letter associated with the object of zdict for the dict semicore
	print "\n"
	print pathlist
	return pathlist
#uses the dictionaries made for znucl, semicore, and quality to make paths and then it prints the paths        





def reader():
	fhi_list = []
	fhi_dict = {}
	z = 0

	for final_path in pathmaker3():
		info_location = os.path.join(final_path, "info.txt")
		info = open(info_location, "r")
		search_names = info.readlines()
		info.close()
		
		for line in enumerate(search_names):
			file_name = line[1].split()
			#print file_name

			for file in file_name:
				if file.endswith('.fhi'):
					fhi_list.append(file)

	print "\nThe .fhi files from info.txt:"
	print fhi_list
	for file in fhi_list:
		z = z + 1
		fhi_dict[z] = file

	return fhi_dict
#when reading the lines of info.txt, it returns a tuple that numbers the lines so this may be useful for the future. 
#For now just prints the files names out of info.txt





def writer():
	fhi_dict = reader()
	print "\nFile names added to pplist:"
		
	pplist = open("Common/pplist", "w")
	#may need to make pplist file first just in case a blank one isn't already there
	#search_pplist = pplist.readlines()

	for key in fhi_dict:
		pplist.write(fhi_dict[key])
		pplist.write("\n")
		print fhi_dict[key]
	
	pplist.close()
#takes fhi_dict from reader(). For each key, it writes it's value (the fhi file names) to pplist in Commmon





def citation_writer():
	citation_file_list = copier()
	current_directory = os.getcwd()
	
        final_citation_file = os.path.join(current_directory, "psp_citation")
        final_citation = open(final_citation_file, "w")
        final_citation.write("Citations:\n")

	for key in zdict:
		citation_file = citation_file_list[key-1]
		#gets location of the znucl's citation file from copier
		zdict[key]
				
		citation = open(citation_file, "r")
                search_citation = citation.readlines()
                citation.close()

                final_citation.write(element_names[znumber_list[key-1]] + ": \n")
		#writes that znucl's symbol to the final citation
		print element_names[znumber_list[key-1]]

                for i, line in enumerate(search_citation):
			if line == line:
                		for l in search_citation[i:]:
					final_citation.write(l)
		
                final_citation.write("\n")
		#writes all of the lines from znucl's citation under it's symbol
	final_citation.close()
		#writes all of citation information about znucls in a file called citation in cwd
	print "The citation has been made in this directory."



def copier():
	current_directory = os.getcwd()
	citation_file_list = []	

	for path in pathmaker3():
		pseudofile_list = os.listdir(path)
		print "\n"
		for file in pseudofile_list:
			file_path = os.path.join(path, file)
			if file.endswith('.txt'):
				print file + " was not copied."
			elif file.startswith('cite'):

				citation_file = os.path.join(path, file)
				citation_file_list.append(citation_file)
			else:
				shutil.copy(file_path, current_directory)
				print file + " was copied."
	print "The pseudo files have been copied into the working directory.\n"	
	print citation_file_list
	return citation_file_list
#takes dict from pathmaker3() in order to know where to copy pseudo files from, finds cwd, then copies pseudo files into Common






#the semicore code:

def semicore_list():
	commons = open("Common/semicore", "r")
	searchs = commons.readlines()
	commons.close()

	y = 0
	sdict = {}
	#print "\nFrom the semicore file:"
	#ssslist = []	
	for index, line in enumerate(searchs):
		semicorestring = index, line 
		semicores_requested = semicorestring[1].split()
		print "\nSemicores requested:"
		print semicores_requested
		#splits string of letters automatically and gets rid of line return and white spaces		
		
		if len(semicores_requested) == 1: 
			for key in pathmaker1():
                	       	sdict[key] = semicores_requested[0]
		#if there's only one semicore requested, add that semicore to sdict for as many znucls as there are
		elif len(semicores_requested) > 1:
			for key in pathmaker1():
			        path = pathmaker1()[key]
        			sslist = os.listdir(path)
        			slist = sorted(sslist)
        			lengths = len(sslist)
	
				semicore = semicores_requested[key-1]
				#index is one less than the order of the keys
				print semicore + " was requested."
					
        			print "\nA znucl's semicore options:"
        			print slist
				
				if semicore in slist:
					sdict[key] = semicore
				#if the requested semicore with that znucl is an option, that option is picked
				else:
					if semicore == "T":
						print "True was requested in Common but was not available."
						sys.exit(1)
					#if the semicore requested was True and it wasn't in slist, exit out of code
					#If T is requested, it must be given or something's wrong
					elif semicore == "F":
						true = slist[0]
						sdict[key] = true
						print "T was picked instead of F."
					#if the semicore requested was False and wasn't in slist, return True
					else:
						print "Something's wrong."
						sys.exit(1)
		else:
			print "There was nothing in the semicore file in Common."
			sys.exit(1)
		#if there's more than one semicore requested, the options need to be checked to make sure the requests are ok
	
		return sdict




def find_greater_or_equal(searched_list, wanted_value):
	options_list = []
	for option in searched_list:
		if option >= wanted_value:
			options_list.append(option)
	if options_list > 0:
		return min(options_list)
	else:
		print "There was no quality available equal to or greater than the asked for value."
                sys.exit(1)
#finds value greater or equal to wanted_value from searched_list		  


def find_next_highest(searched_list):
	return max(searched_list)
	#values are already less than max quality, the highest one just needs to be found.
#finds greateset value less than max quality from searched_list


#the quality code:

def quality_list():
       	print "\nQuality requested in Common file:"

	qdict = {}
	length_options_list = 0
	znucls_num_qlist = []
	new_qlist_numbers = []
	qlist_numbers = []

	commonq = open("Common/pp.quality", "r")
	searchq = commonq.readlines()
	commonq.close()

	for index, line in enumerate(searchq):
		qualitystring = index, line 
		print qualitystring[1]
		quality_asked_for = int(qualitystring[1])
		#grabs the one quality listed in Common and sets it equal to quality_asked_for (which should only be one value)
		for key in pathmaker2():
			path = pathmaker2()[key]
			qqlist = os.listdir(path)
        		qlist = sorted(qqlist)
        		lengthq = len(qqlist)

			print "\nA znucl's quality options:"
			znucls_num_qlist = map(int, qlist)
			print znucls_num_qlist
			 
			closest = find_greater_or_equal(znucls_num_qlist, quality_asked_for)
			#finds out closest value >= to the quality listed in Common so that can be picked
			print "\nThe closest matching option to the quality requested is:"
			print closest
			
			qlist_numbers.append(closest)
			qdict[key] = str(closest)		
			#then for each key in zdict, add a key to qdict with the closest value found above
		#pathmaker2() returns dict of paths that can be used to list of options of quality for each znucl	
	print qdict


	#ecut:
	highest = max(qlist_numbers)		
	print "The highest value of the qualities is " + str(highest)
			
	if highest != quality_asked_for: 
		biggest_quality = str(highest)
        	
        	commone = open("Common/ecut", "w")
        	commone.write(biggest_quality)
        	print "\n" + biggest_quality + " was written to ecut in Common."
        	#takes max quality from qnumber and writes it to ecut file
	#if quality_asked_for isn't the largest value in qnumber_list, rewrite ecut file with largest value from qnumber_list	


	print "Picking best quality option for each znucl.\n"
	for key in pathmaker2():
        	path = pathmaker2()[key]
                qqlist = os.listdir(path)
                qlist = sorted(qqlist)
                lengthq = len(qqlist)

                print "\nJust for the next step. A znucl's options again:"
                znucls_num_qlist = map(int, qlist)
		print znucls_num_qlist

		
		print zdict[key] + " has " + str(qlist_numbers[key-1]) + " currently."

		if qlist_numbers[key-1] <= highest:
			for option in znucls_num_qlist:
				if option <= highest:
					new_qlist_numbers.append(option)
			#for each option in its options, if the option is less than the highest, add it to a list
			if len(new_qlist_numbers) > 0:
				best_option = find_next_highest(new_qlist_numbers)
				qdict[key] = str(best_option)
				print str(best_option) + " was closer to the highest quality.\n"
			#then find the closest option to the highest and replace the current choice in qdict, with that one
		new_qlist_numbers = []
		#if it's chosen option is less than the highest quality picked

	print qdict
	return qdict 
#returns a dictionary to be used in pathmaker3() so it can match each quality with it's znucl and path 






#the znucl code:

zlist = []

for index, line in enumerate(searchz):
	znucl_string = index, line
	print "\nList of everything found in znucl file (in Common):"
        print znucl_string[1]
	znucl_asked_for = znucl_string[1].split()
	for znucl in znucl_asked_for:
		if znucl in alist:
			zlist.append(znucl)

znumber_list = map(int, zlist)

print "The complete list of znucls"
print zlist
#looks through znucl file in Common and grabs the string with requested znucls. If a requested znucl = one of the options in psps, 
#it grabs the znucl from the string and adds it to a list of znucls

print "\nDictionary for znucls:"
x = 0
zdict = {}
for znucl in zlist:
	x = x + 1
	zdict[x] = znucl
#makes the list of znucls into a dictionary so that it's easier to keep track of what's what 

print zdict




#finally everything is called:

pathmaker3()	
	
						
reader()
writer()

citation_writer()
