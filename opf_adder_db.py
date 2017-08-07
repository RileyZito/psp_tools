import sys, sqlite3, os, bz2, hashlib

current_directory = os.getcwd()

database_name = '../psps.db'

def db_check():
        try:
                open(database_name) 
                return True
        #database does exist
        except IOError as e:
                if e.args[0] == 2:
                        print "This database doesn't exist."
			sys.exit(1)
                #if database doesn't exist, warn user and quit 
                else:   
                        print e
                        sys.exit(1)

if db_check() == True:
        db = sqlite3.connect(database_name)
        cursor = db.cursor()




def repeater(file_name):
        file_name_check = raw_input(file_name + "? ")
        if file_name_check != "":
                file_name = raw_input("Re-input file name or [Q]uit:")
		if 'q' in file_name.lower():
			print "User decided to quit."
			sys.exit(1)
	return file_name
#gives user a second chance to enter file name in case they mistyped




def file_name_getter(type):
        file_name = ""

        while os.path.isfile(file_name) == False:

                file_name = raw_input("What's the name of the " + type + " file?")
		if "quit" in file_name:
			print "User decided to quit."
			sys.exit(1)
                file_name = repeater(file_name)

                if os.path.isfile(file_name) == False:
                        print "Invalid file given. Try again or type 'Quit'."

        return file_name
#checks to make sure the user gave a valid file and doesn't let them continue until they enter a valid one




def file_path(only_file, only_path, name):

        if only_file == name:
                print "The file is in the current directory."
                only_path = os.getcwd()
                full_file = os.path.join(only_path, only_file)
        #if user only gives a file name and not a path

        else:
                print "The path to the file was given."
                full_file = os.path.join(only_path, only_file)
        #if user gives a path to a file

        return full_file
#asks user for file then breaks off the name but keeps the path to the file for reading



def file_info_getter(full_file):
        with open(full_file, 'r') as file_info:
                data = file_info.read()
        return data
#opens file and grabs everything from it



def empty(something):
        if something == None or something == "" or something == " " or something == "\n":
                return True
        else:
                return False
#just covers all the different ways a string could be nothing, returns True if string is nothing




print "Make sure you are in the OPF directory."

file_name = file_name_getter(".fhi")

only_path, only_file = os.path.split(os.path.normpath(file_name))
fhi_file = only_file

with open(fhi_file, 'r') as fhi_info:
    data = fhi_info.read()
#opens fhi file and gets everything from it

md5_list = []
m = hashlib.md5(data)
hash = m.hexdigest()
print "\nmd5: "
print hash
#calculates md5

cursor.execute(''' SELECT md5_fhi FROM pseudos ''')
md5_raw_list = cursor.fetchall()

for one_md5 in md5_raw_list:
	if one_md5[0] != None:
                md5 = one_md5[0].encode('ascii', 'ignore')
                md5_list.append(md5)

print "List of current md5's: "
print md5_list
print ""
#grabs all md5's from table


if hash not in md5_list:
        print "md5 fhi is not in pseudo table. Use adder_db to add this entry."
        sys.exit(1)
#if md5 doesn't exist, stop code



def fill_opts_check():
	if empty(raw_fill_db) == True and empty(raw_opts_db) == True:
	        cursor.execute( ''' UPDATE pseudos SET fill_name=?, fill=?, opts_name=?, opts=? WHERE md5_fhi=? ''', (fill_file, fill_data, opts_file, opts_data, hash,))
		print "opts and fill will be added in the database. Note this change will not take effect if you quit at any time."
	#if neither opts or fill is in the databse, the database is updated with both
	elif empty(raw_fill_db) == True or empty(raw_opts_db) == True:
        	if empty(raw_fill_db) == True:
        	        cursor.execute( ''' UPDATE pseudos SET fill_name=?, fill=? WHERE md5_fhi=? ''', (fill_file, fill_data, hash,))
        		print "fill will be added in the database. Note this change will not take effect if you quit at any time."
		#if fill isn't in database, new fill info is added to database
        	else:
        	        fill_db = raw_fill_db.encode('ascii', 'ignore')
        	        if fill_data != fill_db:
        	                print "The fill information does not match the current information in the database."
                	        sys.exit(1)
        	#if fill is in database, new fill info must match
        	if empty(raw_opts_db) == True:
                	cursor.execute( ''' UPDATE pseudos SET opts_name=?, opts=? WHERE md5_fhi=? ''', (opts_name, opts_data, hash,))
        		print "opts will be added in the database. Note this change will not take effect if you quit at any time."
		#if opts isn't in database, new opts info is added to database
        	else:
                	opts_db = raw_opts_db.encode('ascii', 'ignore')
                	if opts_data != opts_db:
                	        print "The opts information does not match the current information in the database."
                	        sys.exit(1)
	#if there's no current info for opts or fill, input what was given

	else:
        	fill_db = raw_fill_db.encode('ascii', 'ignore')
        	opts_db = raw_opts_db.encode('ascii', 'ignore')
        	if opts_data == opts_db and fill_data == fill_db:
        	        print "The opts and fill information is correct."
        	        #then continue on with opts and fill info 

        	else:
        	        print "opts and fill files do not match the current information in the database."
                	sys.exit(1)
#checks and updates fill and opts info in database




cursor.execute( ''' SELECT fill, opts FROM pseudos WHERE md5_fhi=? ''', (hash,))
retrieved = cursor.fetchall()[0]

raw_fill_db = retrieved[0]
raw_opts_db = retrieved[1]
#retrieves opts and fill info from database

file_name = file_name_getter(".fill")

only_path, only_file = os.path.split(os.path.normpath(file_name))
fill_file = only_file
full_fill_file = file_path(only_file, only_path, file_name)
fill_data = file_info_getter(full_fill_file)


file_name = file_name_getter(".opts")

only_path, only_file = os.path.split(os.path.normpath(file_name))
opts_file = only_file
full_opts_file = file_path(only_file, only_path, file_name)
opts_data = file_info_getter(full_opts_file)
#gets opts and fill info from files

fill_opts_check()
cursor.execute( ''' SELECT fill, opts FROM pseudos WHERE md5_fhi=? ''', (hash,))
retrieved = cursor.fetchall()[0]
fill = retrieved[0].encode('ascii', 'ignore')
opts = retrieved[1].encode('ascii', 'ignore')
#retrieves updated/checked opts and fill info from database





numbers = file_info_getter("edges")

list_numbers = numbers.split()

edges_z = int(list_numbers[0])
#for finding the znucl later

N = int(list_numbers[1])
L = int(list_numbers[2])

print "\nN = " + str(N)
print "L = " + str(L)
#getting L and N for database


user_choice = ""

cursor.execute( '''SELECT id FROM core_potential''' )
id_list = cursor.fetchall()
temp_list = []
for id in id_list:
	new_id = id[0]
	temp_list.append(new_id)
id_list = temp_list
print("\nCurrent id's:"),
print id_list
print ""

for id in id_list:
	cursor.execute( '''SELECT N, L, md5_fhi FROM core_potential WHERE id=?''', (id,))
	retrieved = cursor.fetchall()[0]

	try:
		N_db = retrieved[0] + 1 -1 
		L_db = retrieved[1] + 1 -1
		md5_fhi = retrieved[2].encode('ascii', 'ignore')
		print "\nmd5_fhi, N, and L from database: " + md5_fhi + ", " + str(N_db) + ", " + str(L_db)

		if N_db == N and L_db == L and md5_fhi == hash:
			print "This database entry matches the information provided.\n"
			user_choice = raw_input("Would you like to [Q]uit, or [A]dd or [O]verwrite the existing entry?")
			if user_choice == "":
				print "That's not one of the options."
				sys.exit(1)
			chosen_id = id
			break
	except AttributeError and TypeError:
		print "N, L, and/or md5_fhi equaled None. That entry was skipped."			





#functions used in user_choice if/elif statements
###############################################################################################################
def radius_calculator():
	radius = file_info_getter("screen.shells")
	#get radius from screen.shells file in OPF

	radius = float(radius.split()[0])
	radius = round(radius, 2)
	#print "radius is " + str(radius)
	#rounds number from screen.shells to the nearest hundreth 

	return radius
#gets radius		



def core_potential_file_getter(asked_for):
	typat_zs = file_info_getter("typat")
	typat_zlist = typat_zs.split()
	typat_z = int(typat_zlist[edges_z -1])
	#get index from edges for which atom is the one being looked at, then uses that to get the index from typat for which z 	

	z_string = file_info_getter("znucl")
	z_list = z_string.split()
	z = int(z_list[typat_z -1])
	#uses index from typat to get the correct z from the znucl file

	cursor.execute('''SELECT id FROM pseudos WHERE md5_fhi=?''', (hash,))
	main_id = cursor.fetchone()[0]
	cursor.execute('''SELECT z FROM main WHERE id=?''', (main_id,))
	z_db = cursor.fetchone()[0]
	if z != z_db:
		print "Something's wrong. znucl from database does not match znucl from file."
		sys.exit(1)
	#checks that z matches database

	edgename = "z%03in%02il%02i" % (z, N, L)

	possible_files = []
	list_files = os.listdir("zpawinfo")

	for one_file in list_files:
	        if one_file.endswith(edgename):
	                possible_files.append(one_file)
        
	for possible_file in possible_files:
	        if possible_file.startswith("vc_bare"):
        	        vc_bare_file = os.path.join("zpawinfo", possible_file)
        	elif possible_file.startswith("vpseud1"):
        	        vpseud1_file = os.path.join("zpawinfo", possible_file)
        	elif possible_file.startswith("vvallel"):
        	        vvallel_file = os.path.join("zpawinfo", possible_file)
	#finds all files in zpawinfo that endwith the edgename and then finds the specific files needed from those (ex: vc_bare)

	vc_bare_text = file_info_getter(vc_bare_file)
	vpseud1_text = file_info_getter(vpseud1_file)
	vvallel_text = file_info_getter(vvallel_file)

	if asked_for == "vc_bare":
	        return vc_bare_text
	elif asked_for == "vpseud1":
	        return vpseud1_text
	elif asked_for == "vvallel":
	        return vvallel_text
#returns file_text for whichever file was asked for



def text_getter():
	radius = radius_calculator()
	temp = "R" + str(radius)
	if len(temp) == 4:
	        ending = temp + "0"
	else:
	        ending = temp
	#round gets rid of the extra 0 if the number is #.00 so this combines "R" with #.##, accounting for #.0 for radius
	
	list_files = os.listdir("zpawinfo")

	for one_file in list_files:
        	if one_file.startswith("vc_bare") and one_file.endswith(ending):
        	        text_file = os.path.join("zpawinfo", one_file)
	#finds vc_bare file that ends with R#.##

	text = file_info_getter(text_file)
	return text
#gets info for text_file in radii_info using radius 



def core_potential_files_update(id):
	vc_bare_text = core_potential_file_getter("vc_bare")
	vpseud1_text = core_potential_file_getter("vpseud1")
	vvallel_text = core_potential_file_getter("vvallel")
	cursor.execute('''UPDATE core_potential SET vc_bare=?, vpseud1=?, vvallel=? WHERE id=?''', (vc_bare_text, vpseud1_text, vvallel_text, id,))
#updates all core_potential file info in database



def overwrite_shortcut(id):
	overwrite_choice = raw_input("Would you like to: \nOverwrite [A]ll information,\nOverwrite [c]ore_potential files, [r]adius, or [t]ext_file, \nor [Q]uit?")
        if "q" in overwrite_choice.lower():
		print "User decided to quit."
		sys.exit(1)
	elif "a" in overwrite_choice.lower():
                cursor.execute('''DELETE FROM core_potential WHERE id=?''', (id,))
                cursor.execute('''DELETE FROM radii_info WHERE id=?''', (id,))
                #delete the pre-existing information first

                cursor.execute('''INSERT INTO core_potential(id, md5_fhi, N, L) VALUES(?, ?, ?, ?)''', (id, hash, N, L,)) 
                #creates new entry in core_potential

                radius = radius_calculator()
                cursor.execute('''INSERT INTO radii_info(id, radius) VALUES(?, ?)''', (id, radius,))
                #creates a new entry in radii_info

		core_potential_files_update(id)
                #adds info from core_potential files to the new entry in core_potential

                text = text_getter()
                cursor.execute('''UPDATE radii_info SET text_file=? WHERE id=?''', (text, id,))
                #adds the text_file info to new entry in radii_info
		
		print "Overwrote all information."       	
	#creates new entry and fills it out

	elif "t" in overwrite_choice.lower() and "r" in overwrite_choice.lower():
		radius = radius_calculator()
                text = text_getter()
                cursor.execute('''UPDATE radii_info SET radius=?, text_file=? WHERE id=?''', (radius, text, id,))
	
		print "Overwrote text_file and radius."
	#user chose to overwrite radius and text_file

	elif "c" in overwrite_choice.lower():
		core_potential_files_update(id)
		print "Overwrote core_potential files."
	#user chose to overwrite core_potential files

	elif "r" in overwrite_choice.lower(): 
		radius = radius_calculator()
        	cursor.execute('''UPDATE radii_info SET radius=? WHERE id=?''', (radius, id,))
        
		print "Overwrote radius."
	#user chose to overwrite radius	
	elif "t" in overwrite_choice.lower():
		text = text_getter()
        	cursor.execute('''UPDATE radii_info SET text_file=? WHERE id=?''', (text, id,))
        	
		print "Overwrote text_file."
	#user chose to overwrite text_file
#overwrites everything or specifically selected part in database		
############################################################################################





if user_choice == "":
	cursor.execute('''INSERT INTO core_potential(md5_fhi, N, L) VALUES(?, ?, ?)''', (hash, N, L,))	
	#creates new entry in core_potential
	
	id = cursor.lastrowid
	#last id that was entered

	cursor.execute('''INSERT INTO radii_info(id) VALUES(?)''', (id,))
	#creates a new entry in radii_info

	core_potential_files_update(id)
	#adds info from core_potential files to the new entry in core_potential

	radius = radius_calculator()
	text = text_getter()
	cursor.execute('''UPDATE radii_info SET radius=?, text_file=? WHERE id=?''', (radius, text, id,))
	print "A new entry in the database was created."
	#adds the text_file info to new entry in radii_info
#entry doesn't exist, make a new one with the N, L, and md5_fhi under new id, then update all other entries 


elif "q" in user_choice.lower():
	print "User decided to quit."
	sys.exit(1)
#ends code


elif "a" in user_choice.lower():
	id = chosen_id
	print "\nfor id " + str(id) + " all missing information will be filled out."
	needed_list = []
	searched_dict = {}

	cursor.execute( '''SELECT vc_bare FROM core_potential WHERE id=?''', (id,))	
	searched_dict["vc_bare"] = cursor.fetchall()[0][0]
	cursor.execute( '''SELECT vpseud1 FROM core_potential WHERE id=?''', (id,))
	searched_dict["vpseud1"] = cursor.fetchall()[0][0]
	cursor.execute( '''SELECT vvallel FROM core_potential WHERE id=?''', (id,))
	searched_dict["vvallel"] = cursor.fetchall()[0][0]
	#adds names with their text to searched_dict for all core_potential files

	cursor.execute( '''SELECT radius FROM radii_info WHERE id=?''', (id,))
	searched_dict["radius"] = cursor.fetchone()[0]
	cursor.execute( '''SELECT text_file FROM radii_info WHERE id=?''', (id,))
	searched_dict["text_file"] = cursor.fetchall()[0][0]
	#adds names with their text to searched_dict for radius and text_file

	for name in searched_dict:
		print(name),
		thing = searched_dict[name]
		if empty(thing) == True:
			print "is blank."
			needed_list.append(name)
		else:
			print "has " + str(thing)[:10]
	#for all the entries of searched_list that are none, the name of that entry is put into needed_list
	
	if len(needed_list) != 0:
		for needed in needed_list:
                	if needed == "vc_bare" or needed == "vpseud1" or needed == "vvallel":
                        	text = core_potential_file_getter(needed)                       
                        	cursor.execute('''UPDATE core_potential SET ''' + needed + '''=? WHERE id=?''', (text, id,))
                	#for the different core_potential files, their text is added 
                	elif needed == "text_file":
                	        text = text_getter()
                	        cursor.execute('''UPDATE radii_info SET text_file=? WHERE id=?''', (text, id,)) 
                	#text_file info is added
                	elif needed == "radius":
                	        radius = radius_calculator()
                	        cursor.execute('''UPDATE radii_info SET radius=? WHERE id=?''', (radius, id,))
                	#radius is added
	        #what's needed is matched up with info needs to be found, and that info is found.       
		print "\nMissing information was filled out in database."		
	#as long as there's nothing in the database for something, that thing will be added to the needed_list

	else:
		print "There is nothing that needs to be added.\n"
		overwrite_shortcut(id)	
#only update things that are missing from core_potential and radius


elif "o" in user_choice.lower():
	id = chosen_id
	overwrite_shortcut(id)
#overwrites entire file or specifically selected parts using a function


db.commit()
db.close()
