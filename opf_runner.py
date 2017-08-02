import sys, sqlite3, os, bz2, hashlib

db = sqlite3.connect('../psps.db')
cursor = db.cursor()

current_directory = os.getcwd()



def repeater(file_name):
        file_name_check = raw_input(file_name + "? ")
        if file_name_check != "":
                file_name = raw_input("Re-input file name:")
	return file_name
#gives user a second chance to enter file name in case they mistyped




def file_name_getter(type):
        file_name = ""

        while os.path.isfile(file_name) == False:

                file_name = raw_input("What's the name of the " + type + " file?")
                file_name = repeater(file_name)

                if os.path.isfile(file_name) == False:
                        print "Invalid file given. Try again."

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
	if raw_fill_db == None and raw_opts_db == None:
	        cursor.execute( ''' UPDATE pseudos SET fill=?, opts=? WHERE md5_fhi=? ''', (fill_data, opts_data, hash,))
	#if neither opts or fill is in the databse, the database is updated with both
	elif raw_fill_db == None or raw_opts_db == None:
        	if raw_fill_db == None:
        	        cursor.execute( ''' UPDATE pseudos SET fill=? WHERE md5_fhi=? ''', (fill_data, hash,))
        	#if fill isn't in database, new fill info is added to database
        	else:
        	        fill_db = raw_fill_db.encode('ascii', 'ignore')
        	        if fill_data != fill_db:
        	                print "The fill information does not match the current information in the database."
                	        sys.exit(1)
        	#if fill is in database, new fill info must match
        	if raw_opts_db == None:
                	cursor.execute( ''' UPDATE pseudos SET opts=? WHERE md5_fhi=? ''', (opts_data, hash,))
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




with open("edges", 'r') as edges:
	numbers = edges.read()

list_numbers = numbers.split()

N = int(list_numbers[1])
L = int(list_numbers[2])

print "\nN = " + str(N)
print "L = " + str(L)



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
			chosen_id = id
			break
	except AttributeError and TypeError:
		print "N, L, and/or md5_fhi equaled None. That entry was skipped."			





def radius_calculator():
	radius = file_info_getter("screen.shells")
	#get radius from screen.shells file in OPF

	radius = float(radius.split()[0])
	radius = round(radius, 2)
	print "radius is " + str(radius)
	#rounds number from screen.shells to the nearest hundreth 

	return radius
#gets radius		



def core_potential_file_getter(asked_for):
	z = file_info_getter("znucl")
	z = int(z.split()[0])

	edgename = "z%03in%02il%02i" % (z, N, L)

	possible_files = []
	list_files = os.listdir("zpawinfo")

	for one_file in list_files:
	        if one_file.endswith(edgename):
	                possible_files.append(one_file)
        
	for possible_file in possible_files:
	        if possible_file.startswith("vc_bare"):
        	        print possible_file
        	        vc_bare = os.path.join("zpawinfo", possible_file)
        	elif possible_file.startswith("vpseud1"):
        	        print possible_file
        	        vpseud1 = os.path.join("zpawinfo", possible_file)
        	elif possible_file.startswith("vvallel"):
        	        print possible_file
        	        vvallel = os.path.join("zpawinfo", possible_file)
	#finds all files in zpawinfo that endwith the edgename and then finds the specific files needed from those (ex: vc_bare)

	vc_bare_text = file_info_getter(vc_bare)
	vpseud1_text = file_info_getter(vpseud1)
	vvallel_text = file_info_getter(vvallel)

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
        	        print one_file
        	        text_file = os.path.join("zpawinfo", one_file)
	#finds vc_bare file that ends with R#.##

	text = file_info_getter(text_file)
	return text
#gets info for text_file in radii_info using radius 





if user_choice == "":
	id = max(id_list) + 1
	print id

	cursor.execute('''INSERT INTO core_potential(id, N, L) VALUES(?, ?, ?)''', (id, N, L,))	
	#creates new entry in core_potential
	
	radius = radius_calculator()
	cursor.execute('''INSERT INTO radii_info(id, radius) VALUES(?, ?)''', (id, radius,))
	#creates a new entry in radii_info

	vc_bare_text = core_potential_file_getter("vc_bare")
	vpseud1_text = core_potential_file_getter("vpseud1")
	vvallel_text = core_potential_file_getter("vvallel")
	cursor.execute('''UPDATE core_potential SET vc_bare=?, vpseud1=?, vvallel=? WHERE id=?''', (vc_bare_text, vpseud1_text, vvallel_text, id,))
	#adds info from core_potential files to the new entry in core_potential

	text = text_getter()
	cursor.execute('''UPDATE radii_info(text_file) VALUES(?) WHERE id=?''', (text,))
	#adds the text_file info to new entry in radii_info
#entry doesn't exist, make a new one with the N, L, and md5_fhi under new id, then update all other entries 


elif "q" in user_choice.lower():
	print "User decided to quit."
	sys.exit(1)
#ends code


elif "a" in user_choice.lower():
	id = chosen_id
	print "for id, " + str(id) + ", all missing information will be filled out."
	index_list = []
	needed_list = []

	cursor.execute( '''SELECT vc_bare, vpseud1, vvallel FROM core_potential WHERE id=?''', (id,))
	core_potential_list = cursor.fetchall()
	cursor.execute( '''SELECT radius, text_file FROM radii_info WHERE id=?''', (id,))
	radii_info_list = cursor.fetchall()
	searched_list = radii_info_list + core_potential_list
	#gets list of everything for id in both tables

	for thing in searched_list:
		if thing[0] == None or thing[0] == "":
			index_list.append(searched_list.index(thing))
	#for all the entries of searched_list that are none, the index is put into a list for that entry
	
	if len(index_list) != 0:
		print index_list
		print "0 = vc_bare, 1 = vspeud1, 2 = vvallel, 3 = radius, 4 = text_file"
		print "Each index requested still needs to be filled in.\n"
			
		for index in index_list:
			if index == 0:
				item = "vc_bare"
			elif index == 2:
				item = "vspeud1"
			elif index == 3:
				item = "vvallel"
			elif index == 4:
				item = "radius"
			elif index == 5:
				item = "text_file"
			needed_list.append(item)
	else:
		print "There is nothing that needs to be added. Run the code again and choose Overwrite if you wish to overwrite any of these existing entries."	
	#as long as there's nothing in the database for something, that thing will be added to the needed_list

	for needed in needed_list:
		if needed == "vc_bare" or needed == "vpseud1" or needed == "vvallel":
			text = core_potential_file_getter(needed)			
			cursor.execute('''UPDATE core_potential SET''' + needed + '''=? WHERE id=?''', (text, id,))
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
#only update things that are missing from core_potential and radius


elif "o" in user_choice.lower():
	id = chosen_id
	print id
	#fill this shit out my dude (but later after lunch)


#delete that entry? or just update everything


#cursor.execute( '''UPDATE core_potential SET N=?, L=? WHERE id=? ''', (N, L, id,))






db.commit()
db.close()
