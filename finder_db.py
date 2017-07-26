import sqlite3, os, sys, bisect, shutil

db= sqlite3.connect('psp.db')
cursor = db.cursor()


#just to make sure the main table is working like it should:

print('SELECT * FROM main')
cursor.execute(''' SELECT * FROM main ''')
print(cursor.fetchall())




#znucl code:

print('\nSELECT z FROM main')
cursor.execute(''' SELECT z FROM main ''')
#it looks in main table to find znucls available          
dblist_znucls = []
result = cursor.fetchone()
while result is not None:
	dblist_znucls.append(result[0])
	result = cursor.fetchone()
#iterates through znucls in main and then makes a list

db_zlist = sorted(dblist_znucls)
db_str_zlist = map(lambda x:str(x), db_zlist)
#lists everything in pseudo directory    

commonz = open("Common/znucl", "r")
searchz = commonz.readlines()
commonz.close()

#looks at znucl file in Common


print "Available elements (by atomic number):"
print db_zlist

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

already_printed = []

for number in db_zlist:
        if number in element_names and number not in already_printed:
                print "Atomic number " + str(number) + " is " + element_names[number]
        elif number not in element_names:
                print "Name has not been inputed yet for atomic number " + str(number)
	already_printed.append(number)
#for each of the znucl options listed. if the atomic number is in element_names, print the element name, else, say it's n$







#An attempt to shorten stuff:

statement_list = []
def print_once(statement):
        if statement not in statement_list:
                statement_list.append(statement)
                print statement
#should print each thing it's called on only once






#the final pathmaking code:

def file_writer():
	citation_dict = {}
	id_list = []
	quality = quality_list()
        semicore = semicore_list()
	current_directory = os.getcwd()

	for key in zdict:
		cursor.execute( ''' SELECT id FROM main WHERE z=? AND qf=? AND semicore=? ''', (zdict[key], quality[key], semicore[key]))	
		znucl_id = cursor.fetchone()[0]

		id_list.append(znucl_id)
	#creates list of all the ids for each znucl

	print "\nList of ids for each znucl:"		
	print id_list

	for key in zdict:
		znucl_id = id_list[key-1]
	

		#fhi:
		cursor.execute( ''' SELECT fhi_name FROM pseudos WHERE id=? ''', (znucl_id,))

		retrieved = cursor.fetchone()[0]
		fhi_name =  retrieved.encode('ascii', 'ignore')
		print "fhi file name is: " + fhi_name

		cursor.execute( ''' SELECT fhi FROM pseudos WHERE id=? ''', (znucl_id,))

		retrieved = cursor.fetchall()[0]
		fhi_text = str(retrieved[0])	
		#gets fhi file name and text from database and saves it as variables

		fhi_location = os.path.join(current_directory, fhi_name)
		with open(fhi_location, "w") as fhi:
			fhi.write(fhi_text)
		print fhi_name + " was written.\n"
		#writes found fhi information to a created fhi file with found fhi name


		#UPF:
		cursor.execute( ''' SELECT upf_name FROM pseudos WHERE id=? ''', (znucl_id,))

		retrieved = cursor.fetchone()[0]
                upf_name =  retrieved.encode('ascii', 'ignore')
                print "UPF file name is: " + fhi_name

                cursor.execute( ''' SELECT upf FROM pseudos WHERE id=? ''', (znucl_id,))

                retrieved = cursor.fetchall()[0]
                upf_text = str(retrieved[0])    
                #gets upf file name and text from database and saves it as variables

                upf_location = os.path.join(current_directory, upf_name)
                with open(upf_location, "w") as upf:
                        upf.write(upf_text)
                print upf_name + " was written.\n"
                #writes found upf information to a created upf file with found upf name

	
		#znucl's citation:
		cursor.execute( ''' SELECT citation FROM pseudos WHERE id=? ''', (znucl_id,))

                retrieved = cursor.fetchall()[0]
                citation_text = str(retrieved[0])
		citation_dict[key] = citation_text
		#creates a dictionary of the text for each znucl's citation
	#for each znucl, it uses it's id to write pseudo files
	
	#citation with everything:
	citation_location = os.path.join(current_directory, "psp_citation")

        with open(citation_location, "w") as citation:
		citation.write("Citations:\n\n")
		for key in zdict:
			citation.write(zdict[key] + ":\n")
                	citation.write(citation_dict[key])
			citation.write("\n")
		#writes citation info for each znucl
        #writes all of the citation information to a created citation file 






#the semicore code:

def semicore_list():
        commons = open("Common/semicore", "r")
        searchs = commons.readlines()
        commons.close()

        y = 0
        sdict = {}
           
        for index, line in enumerate(searchs):
                semicorestring = index, line
                semicores_requested = semicorestring[1].split()
                print_once("\nSemicores requested:")
                print_once(semicores_requested)
                #splits string of letters automatically and gets rid of line return and white spaces            

                if len(semicores_requested) == 1:
			one_semicore = semicores_requested[0]
			semicores_requested = []
			for key in zdict:
                                semicores_requested.append(one_semicore)
		#if there's only one semicore requested, add that semicore to semicores_requested for as many znucls as there are
		elif len(semicores_requested) < 1:
                        print "There was nothing in the semicore file in Common."
                        sys.exit(1)
                #if there's no semicore requested, end

		for key in zdict:
			znucl = (zdict[key],)
			#print('\nSELECT semicore FROM main WHERE z = ' + zdict[key])
			cursor.execute(''' SELECT semicore FROM main WHERE z=?''', znucl)
			#for znucl, it looks in main table to find semicores available		
	
			dblist_semicores = []
			result = cursor.fetchone()
			
			while result is not None:
				dblist_semicores.append(result[0].encode('ascii', 'ignore'))
				result = cursor.fetchone()
			#iterates through semicores available in main and then makes a list
                               
			db_slist = sorted(dblist_semicores)
                        length_db_slist = len(dblist_semicores)
			#list of semicore options for the znucl and length of list just in case
        
                        semicore = semicores_requested[key-1]
                        #index is one less than the order of the keys
			print "\n" + semicore + " was requested for " + zlist[key-1]

                        print "Its semicore options:"
			print db_slist

                        if semicore in db_slist:
                        	sdict[key] = semicore
				print semicore + " was chosen."
                        #if the requested semicore is an option, that option is picked
                        else:
                        	if semicore == "T":
                        		print "True was requested in Common but was not available."
                        		sys.exit(1)
                                #if the semicore requested was True but it wasn't an option, exit out of code
                                #If T is requested, it must be given
                                elif semicore == "F":
                                	sdict[key] = db_slist[0]
                                        print "NOTICE. T was picked instead of F."
                                #if the semicore requested was False but it wasn't an option, return True
                                else:
                                	print "Something's wrong."
                                	sys.exit(1)
			#the requested semicore wasn't an option
		#with the however many long list, it will figure what semicores will be picked

                print_once("\nSemicore dictionary:")
                print_once(sdict)
                return sdict





def find_greater_or_equal(searched_list, wanted_value):

        value_found = bisect.bisect_left(searched_list, wanted_value)
        if value_found == len(searched_list):
                print "There was no quality available equal to or greater than the asked for value."
                sys.exit(1)
        return searched_list[value_found]
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
	qlist_numbers = []
        new_qlist_numbers = []

        commonq = open("Common/pp.quality", "r")
        searchq = commonq.readlines()
        commonq.close()

        for index, line in enumerate(searchq):
                qualitystring = index, line
                print_once(qualitystring[1])
                quality_asked_for = int(qualitystring[1])
                #grabs the one quality listed in Common and sets it equal to quality_asked_for (which should only be one $

		sdict = semicore_list()
                for key in zdict:
                        znucl = zdict[key]
			semicore = sdict[key].decode('utf-8', 'ignore')

                        print('\nSELECT semicore FROM main WHERE z = ' + zdict[key] + ' AND semicore = ' + sdict[key])
                        cursor.execute(''' SELECT qf FROM main WHERE z=? AND semicore=? ''', (znucl, semicore,))
                        #for znucl, it looks in main table to find semicores available          

                        dblist_qualities = []
                        result = cursor.fetchone()

                        while result is not None:
                                dblist_qualities.append(result[0])
                                result = cursor.fetchone()
                        #iterates through semicores available in main and then makes a list

                        db_qlist = sorted(dblist_qualities)
                        length_db_qlist = len(dblist_qualities)
                        #list of semicore options for the znucl and len


                        "\nA znucl's quality options:"
                        db_num_qlist = map(int, db_qlist)
                        print db_num_qlist

                        closest = find_greater_or_equal(db_num_qlist, quality_asked_for)
                        #finds out closest value >= to the quality listed in Common so that can be picked
                        print "\nThe closest matching option to the quality requested is:"
                        print closest

			qlist_numbers.append(closest)
                        qdict[key] = str(closest)

                        #then for each key in zdict, add a key to qdict with the closest value found above
        #qnumber_list holds each of the chosen values for quality
        print qdict


        
	#ecut:
	highest = max(qlist_numbers)
	print "The highest value of the qualities is " + str(highest)

	if highest != quality_asked_for:
                biggest_quality = str(highest)

                commone = open("Common/ecut", "w")
                commone.write(biggest_quality)
                print "\n" + biggest_quality + " was written to ecut in Common.\n"
                #takes max quality from qnumber and writes it to ecut file
        #if quality_asked_for isn't the largest value in qnumber_list, rewrite ecut file with largest value from qnumber_



	print "Checking to make sure the best option for each znucl was picked.\n"
	for key in zdict:
		znucl = zdict[key]
		semicore = sdict[key].decode('utf-8', 'ignore')
		cursor.execute(''' SELECT qf FROM main WHERE z=? AND semicore=? ''', (znucl, semicore,))
		#for znucl, it looks in main table to find semicores available          

		dblist_qualities = []
		result = cursor.fetchone()

		while result is not None:
			dblist_qualities.append(result[0])
			result = cursor.fetchone()
		#iterates through semicores available in main and then makes a list

		db_qlist = sorted(dblist_qualities)

		"A znucl's quality options:"
		db_num_qlist = map(int, db_qlist)
		print db_num_qlist
		#repeated to get the znucl's options
	

		print zdict[key] + " has " + str(qlist_numbers[key-1]) + " currently."

		if qlist_numbers[key-1] <= highest:
			for option in db_num_qlist:
				if option <= highest:
					new_qlist_numbers.append(option)
			#for each option in its options, if the option is less than the highest, add it to a list
			if len(new_qlist_numbers) > 0: 
				best_choice = find_next_highest(new_qlist_numbers)
				qdict[key] = str(best_choice)
				print str(best_choice) + " was closer to the highest quality.\n"
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
                if znucl in db_str_zlist:
                        zlist.append(znucl)
		else:
			print "It's still wrong."
			zlist.append(znucl)
		
znumber_list = map(int, zlist)

print "The complete list of znucls"
print zlist
#looks through znucl file in Common and grabs the string with requested znucls. If a requested znucl = one of the options$
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

file_writer()

db.close()
