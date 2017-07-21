import os, sys, shutil
from distutils.dir_util import copy_tree

commona = open("Common/pp.dir", "r")
searcha = commona.readlines()
commona.close()

for index, line in enumerate(searcha):
        dir_string = index, line
        dir_asked_for = dir_string[1].split()
        for dir in dir_asked_for:
                absolute_path = dir
#search pp.dir in Common to get the absolute path, a will use this

#a = os.path.join(absolute_path)
a = os.path.join("tester/psps")
aalist = os.listdir(a)
alist = sorted(aalist)
numa = range(1, 121)

print "Current elements (by atomic number):"
print alist
print a

element_names = {
        1: "H",
        2: "He",
        3: "Li",
        4: "Be",
        5: "B",
        6: "C",
        7: "N",
        8: "O",
        9: "F",
        10: "Ne",
        11: "Na",
        12: "Mg",
        13: "Al",
        14: "Si",
        15: "P",
        16: "S",
        17: "Cl",
        18: "Ar",
        19: "K",
        20: "Ca",
        21: "Sc",
        22: "Ti",
        23: "V",
        24: "Cr",
        25: "Mn",
        26: "Fe",
        27: "Co",
        28: "Ni",
        29: "Cu",
        30: "Zn",
#more names need to be inputed  
}
#list of atomic numbers with their corresponding symbol

for number in map(int, alist):
        if number in element_names:
                print "Atomic number " + str(number) + " is " + element_names[number]
        else:
                print "Name has not been inputed yet for atomic number " + str(number)
#for each of the znucl options listed. if the atomic number is in element_names, print the element name, else, say it's not t$






def filecopy():
        finallist = os.listdir(finalpath)
        print "In final directory: " + finalpath + "\n"
        #takes finalpath of where the user wants to add files to and lists current files in it and what it is
        #copy code from finder.py to decide if it was a valid input and such

        print "Before you copy files, check that you have .fhi, .fhi.UPF, opts, fill, and the citation."
        delay_and_check = raw_input("Are you ready to proceed? [Q]uit will stop the progam:")
        if "q" in delay_and_check.lower():
                sys.exit(1)
        #just makes sure they have all the files needed before they're copied

	userchoice = " "
	
	while "stop" not in userchoice.lower():
        	userchoice = raw_input("Where is the pseudofile you would like to copy? Type stop when finished or [Q]uit:")
		if os.path.isfile(userchoice) == True:
			pseudofile = userchoice
			shutil.copy(pseudofile, finalpath)

		elif "q" in userchoice[0].lower():
			print "Quitting."
			sys.exit(1) 
		
		elif "stop" in userchoice[:4].lower():
                	print "Stopped."

		else:
			print "That file does not exist. Re-type the file name."				
        	#allows user to pick as many files as they would like and then stop. they have to input each name.
		
#just checks files to see if they already exist in finalpath and whether to overwrite them, it's used in quality code





def repeater(file_name):
	file_name_check = raw_input(file_name + "? ")
	if file_name_check != "":
		file_name = raw_input("Re-input file name:")
#gives user a second chance to enter file name in case they mistyped


def filewriter():
        print "\nPlease write which file is which."

        fhi = raw_input("What file is the .fhi?")
        repeater(fhi)

        UPF = raw_input("What file is the .fhi.UPF?")
        repeater(UPF)

        opts = raw_input("What file is the .opts?")
        repeater(opts)

        fill = raw_input("What file is the .fill?")
        repeater(fill)

        cite = raw_input("What file is the citation?")
        repeater(cite)
	#for each file type it asks the user what the name for that type is. Ex: for fhi file, user might input ti.fhi

        info_location = os.path.join(finalpath, "info.txt")
        info = open(info_location, "w")
        info.write(fhi + "\n" + UPF + "\n" + opts + "\n" + fill + "\n" + cite)
        info.close()
#creates info.txt and writes all of the different file names to it





#znucl code:

def element():
	i = int(input("Enter which element you would like to add (by atomic number):"))
	if i in numa:
		return i
	else:
		return 0
		sys.exit(0)
	

nucl = element()
znucl = str(nucl)

s = os.path.join(a, znucl)


if znucl not in alist:
        os.makedirs(s)
	sc = True
	#user creates a new directory
elif znucl in alist:
        inp = raw_input("\nWould you like to [C]ontinue, [O]verwrite, or [Q]uit:")
        if "q" in inp.lower():
                print "Quitting."
		sys.exit(1)
        elif "o" in inp.lower():
                overwrite = raw_input("Warning, this will overwrite an already existing directory. Type yes to overwrite:")
        	if "y" in overwrite[0]:
			shutil.rmtree(s)         
			os.makedirs(s)
			print "The directory was overwritten."
			semicores_exist = False
		else:
			print "The directory was kept as is."
			semicores_exist = True
	#Allows them to overwrite but warns them  
	else:
		print "Continuing in " + znucl + "\n"
        	semicores_exist = True
        #user continues in already existing directory       
#checks if znucl asked for already exists and goes from there






#long code for semicore:

T = os.path.join(s, "T")
F = os.path.join(s, "F")
#for later use with the user either going into False or True

def continuer():
	 inpu = raw_input("Which would you like to continue in (T or F)?")
         if "t" in inpu.lower():
         	return "1"
         elif "f" in inpu.lower():
		return "2"
         else:
                print "That's not an option."
                sys.exit(0)
	#if True and False exist, user has to decide which one to enter


#determining semicore:

if semicores_exist == False:
	scinput = raw_input("Is semicore an option for this element?")
	if "y" in scinput:
		print "Adding T and F to " + znucl + " directory."
		os.makedirs(T)
		os.makedirs(F)
		print "Continuing on in 'T'. Make sure to add to 'F' later."
		q = os.path.join(s, "T")
	#the user chooses to have T and F in new znucl directory
	elif "y" not in scinput:
		print "Adding F to " + znucl + " directory."
		os.makedirs(F)
		q = os.path.join(s, "F")
	#the user chooses to have only F in new znucl directory
	else:
		print "Something went wrong."
		sys.exit(0)
#the user made a new directory for an element so they decide if there's T and F or just F as options

elif semicores_exist == True:
	slist = os.listdir(s)
	lengths = len(slist)

	if lengths == 0:
		scinput = raw_input("Would you like to add 'T' as an option?")
                if "y" in scinput:
                        print "Adding 'T' to " + znucl + " directory."
                        os.makedirs(T)
			os.makedirs(F)
			print "Both 'T' and 'F' have been added. Continuing to 'T', make sure to add to 'F' later."
                        #user adds True and False to directory
			q = os.path.join(s, "T")
			#there's just an empty False for now. This puts trust in users to not just leave an empty False
		elif "y" not in scinput:
                	print "Adding only 'F' to "  + znucl + " directory."
                        os.makedirs(F)
			q = os.path.join(s, "F")
			#user adds only False to directory
	#if there's nothing in the znucl directory, the user has to pick what gets added

	elif lengths == 1:
		scinput = raw_input("Would you like to add 'T' as an option?")
		if "y" in scinput:
			print "Adding 'T' to " + znucl + " directory."
			os.makedirs(T)
			#user adds True to directory
			q = os.path.join(s, "T")
			#user is directed to True because they gotta add stuff to it
		elif "y" not in scinput:
			print "Continuing on into 'F'"
			q = os.path.join(s, "F")
		#user doesn't add anything and continues into False	
	#False is only currently existing option, user has to choose to add True or not

	elif lengths == 2:
		T_link = os.path.join(s, "T")
		if os.path.islink(T_link) == True:
			print "Currently True doesn't make sense for this element." 
			overwrite_link = raw_input("Would you like to [A]dd 'T' or [C]ontinue into 'F'?")
			if "a" in overwrite_link.lower():
				os.unlink(T_link)
				os.makedirs(T)
				q = os.path.join(s, "T")
			#adds T overtop of the symbolic link

			elif "c" in overwrite_link.lower():
				print "Continuing into 'F'"
				q = os.path.join(s, "F")
			#user continues into F
		#if T is actually a symlink, they have to choose to overwrite it or continue

		else:
			print "True and False already exist."
			if continuer() == "1":
				print "Continuing into 'T'"
			        q = os.path.join(s, "T")
			else:
				print "Continuing into 'F'"
        			q = os.path.join(s, "F")

		#directs user to method that decides if they are going in True or False 
	
	else:
		print "Something's wrong with the directory."
		sys.exit(0)
#the directory already existed for their choice of znucl, so now they need to decide if they will add T to semicore,
#continue on in T or F if the directory has both, or to continue on in F (or exit i guess)






#quality code:

qqlist = os.listdir(q)
qlist = sorted(qqlist)
lengthq = len(qlist)
numq = map(int, qqlist)


if lengthq == 0:
	print "\nThere are no pre-existing directories"
	userinput = "a"
else:
	print "\nThe available options are:" 
	print qlist
	userinput = raw_input("For quality, would you like to [A]dd, [O]verwrite, [C]ontinue, or [Q]uit:")
#if the list is empty, it tells the user there are none and makes them add a quality.
#if the list has stuff, it lists them and then asks the user if they would like to add another quality.

if "q" in userinput.lower():
	print "You decided to quit."
	sys.exit(1)
	#quits

elif "o" in userinput.lower():
	numinput = int(input("What quality would you like to overwrite?"))
	if numinput in numq:
        	finalpath = os.path.join(q, str(numinput))
        	shutil.rmtree(finalpath)
        	os.makedirs(finalpath)
        	print str(numinput) + " was overwritten."
        	#overwrites directory
        	filecopy()
        	filewriter()
        #the user decides to overwrite pre-existing directory and they copy their files in

	if numinput not in numq:
		print "That quality does not currently exist.\n"
		add_quality = raw_input("What would you like to do? [A]dd the quality, [O]verwrite a different one, or [Q]uit:")
		if "q" in add_quality.lower():
			print "You decided to quit."
			sys.exit(1)
			#quits

		elif "a" in add_quality.lower():
			finalpath = os.path.join(q, str(numinput))
	                os.makedirs(finalpath)
	                print str(numinput) + " was added."
	                #directory is made
	                filecopy()
	                filewriter()
		#if the user's choice of quality does not exist, the directory is made. files are copied 
			
		elif "o" in add_quality.lower():
			numinput = int(input("What quality would you like to overwrite?"))
		        if numinput in numq:
                		finalpath = os.path.join(q, str(numinput))
                		shutil.rmtree(finalpath)
                		os.makedirs(finalpath)
                		print str(numinput) + " was overwritten."
                		#overwrites directory
                		filecopy()
                		filewriter()
			elif numinput not in numq:
				print "That quality does not exist."
				sys.exit(1)
		#user gets a second chance to overwrite a quality directory. If they don't choose one that exists, it ends	
	#the user chose a quality that didn't exist so they have to pick what to do from there


elif "a" in userinput.lower():
	numinput = int(input("What quality would you like to add?"))

	if numinput not in numq:
		finalpath = os.path.join(q, str(numinput))
		os.makedirs(finalpath)
		print str(numinput) + " was added."
		#directory is made
		filecopy()
		filewriter()
	#if the user's choice of quality does not exist, the directory is made. files are copied	
	elif numinput in numq:
		print "That quality already exists."
		owquality = raw_input("Would you like to overwrite the pre-existing directory " + str(numinput) + ":") 
		if "y" in owquality[0]:
			finalpath = os.path.join(q, str(numinput))
			shutil.rmtree(finalpath)
                        os.makedirs(finalpath)
                        print "The directory was overwritten."
			#overwrites directory
                        filecopy()
			filewriter()
		#the user decides to overwrite pre-existing directory and they copy their files in
                else:
                        print "The directory was kept as is."
                        finalpath = os.path.join(q, str(numinput))
			#continue in pre-existing directory		
			filecopy()
			filewriter()
		#if the user decides not to change quality, they continue in the pre-existing directory and copy files
#if user said they wanted to add another quality

elif "c" in userinput.lower():
	ask = int(input("Which quality would you like to continue into?"))
	
#########################################################################################################
	def qual():
        
	#repeat variable list if needed here

        	if ask in numq:
                	return str(ask)
        	#if the user's input existed in the list, that option is chosen
        	elif lengthq == 1:
        	        return qlist[0]
        	#will choose the only option because there is only 1 directory listed by qlist
        	elif ask > 0 or ask < 150:
                	if ask <= 40:
                        	outcome = 40
                        	if outcome in numq:
                                	return str(outcome)
                        	else:
                                	return "0"
                        	#will choose 40 if list is longer and user didn't give an exact number, as long as 40 matches the list
                	elif ask > 40 and ask <= 80:
                        	outcome = 80
                        	if outcome in numq:
                                	return str(outcome)
                        	else:
                                	return "0"
                        	#will choose 80 if list is longer and user didn't give an exact number, as long as 80 matches the list 
                	elif ask > 80:
                        	outcome = 100
                        	if outcome in numq:
                                	return str(outcome)
                        	else:
                                	return "0"
                        	#will choose 100 if list is longer and user didn't give an exact number, as long as 100 matches the list
        	#if the users input exists in the quality directory
        	else:
                	return "0"
                	#ends code if it's not valid 

	checkask = ask
	#asks for input. It was necessary to remove it from qual() for checker(). checkask is just to avoid problems within checker()
	firstq = qual()

	def checker():
        	if firstq == "0":
                	print "No valid quality was returned. Try again."
                	sys.exit(0)
                	#if the user's input didn't end up on any of the available options, the code ends.
        	elif str(checkask) != firstq:
                	print "Your request, " + str(checkask) + ", was not available. " + firstq + " was picked instead."
                	retry = raw_input("Type 'retry' to re-enter quality or accept value and continue:")
                	if "re" in retry.lower():
                	        ask = int(input("What quality would you like now:"))
                	        qual()
                	        quality = qual()
                	elif "quit" in retry.lower():
                        	print "Code ended."
                        	sys.exit(0)
                	else:
                        	print firstq + " was chosen."
                        	quality = qual()
        	else:
        	        quality = qual()
	#checks to make sure user's input was valid and if it matched the listed options. If it doesn't match, they're notified.

	checker()
	quality = qual()

#########################################################################################################	
#using finder.py code to check that quality made sense

	finalpath = os.path.join(q, quality)
	filecopy()
	filewriter()
#if user picked a valid quality, they continue into that quality and copy files 
