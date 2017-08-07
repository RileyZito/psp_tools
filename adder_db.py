import sys, sqlite3, os, hashlib


database_name = 'psps.db'

def db_creator():
	try:
		open(database_name)
		return False
	#database does exist
	except IOError as e:
		if e.args[0] == 2:
			user_continue = raw_input("The database doesn't exist. Would you like to [C]reate it or [Q]uit?\n")
			if "q" in user_continue.lower():
				print "User decided to quit."
				sys.exit(1)
			elif "c" in user_continue.lower():
				return True	
	
		#if database doesn't exist, warn user and create it 
		else:
			print e
			sys.exit(1)

if db_creator() == True:
	print "\nDatabase will be created."
	db = sqlite3.connect(database_name)
	cursor = db.cursor()
	cursor.execute(''' CREATE TABLE main( id INTEGER PRIMARY KEY, z INTEGER, qf INTEGER, semicore TEXT ) ''' )
	cursor.execute(''' INSERT INTO main(id, semicore ) VALUES(?, ?)''', (0, "don't delete this entry.",))
	#creates id of 1 automatically
	cursor.execute(''' CREATE TABLE pseudos( id INTEGER, md5_fhi TEXT PRIMARY KEY, fhi_name TEXT, fhi TEXT, md5_upf TEXT, upf_name TEXT, upf TEXT, citation TEXT, opts_name TEXT, opts TEXT, fill_name TEXT, fill TEXT) ''' )
	cursor.execute(''' CREATE TABLE core_potential( id INTEGER PRIMARY KEY, md5_fhi TEXT, N INTEGER, L INTEGER, vc_bare TEXT, vpseud1 TEXT, vvallel TEXT) ''')
	cursor.execute(''' INSERT INTO core_potential( id, vc_bare) VALUES(?, ?)''', (0, "don't delete this entry.",))
	cursor.execute(''' CREATE TABLE radii_info( id INTEGER, radius REAL, text_file TEXT ) ''')
	#creates all the different tables needed
	print "psps.db tables have been created."
#creates database if it doesn't exist

elif db_creator() == False:
	db = sqlite3.connect(database_name)
        cursor = db.cursor()
#connects to existing database




def repeater(file_name):
        file_name_check = raw_input(file_name + "? ")
        if file_name_check != "":
                file_name = raw_input("Re-input file name or [Q]uit:\n")
		if "q" in file_name.lower():
			print "User decided to quit."
			sys.exit(1)
	return file_name
#gives user a second chance to enter file name in case they mistyped




def file_name_getter(type):
	file_name = ""
	
	while os.path.isfile(file_name) == False:
	
		file_name = raw_input("What's the name of the " + type + " file?\n")
		if "quit" in file_name.lower():
			print "User decided to quit."
			sys.exit(1)
		file_name = repeater(file_name)

        	if os.path.isfile(file_name) == False:
                	print "Invalid file given. Try again or type 'Quit'.\n"

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





#for fhi:

file_name = file_name_getter(".fhi")

only_path, only_file = os.path.split(os.path.normpath(file_name))

fhi_file_name = only_file
fhi_file = file_path(only_file, only_path, file_name)

if file_name != fhi_file_name:
	print fhi_file_name
	#gets name of file, and path to the file

data = file_info_getter(fhi_file)

md5_list = []
m = hashlib.md5(data)
hash = m.hexdigest()
print "\nmd5: " + hash
#calculates md5

cursor.execute(''' SELECT md5_fhi FROM pseudos ''')
md5_raw_list = cursor.fetchall()

for one_md5 in md5_raw_list:
	if one_md5[0] != None:
		md5 = one_md5[0].encode('ascii', 'ignore')
        	md5_list.append(md5)

print "List of current md5's: " 
print md5_list
#grabs all md5's from table


if hash in md5_list:
	print "\nmd5 already exists in pseudos table. Something is wrong."
	sys.exit(1)
#if md5 exists, stop code

cursor.execute( '''INSERT INTO pseudos( fhi_name, md5_fhi ) VALUES(?, ?) ''', (fhi_file_name, hash,))
#adds new column in pseudos with md5 from fhi file and the fhi's file name

cursor.execute( ''' UPDATE pseudos SET fhi=? WHERE fhi_name=? ''', (data, fhi_file_name,))
#inserts everything from fhi file and inserts it into fhi in pseudos





#for UPF:

file_name = file_name_getter(".UPF")

only_path, only_file = os.path.split(os.path.normpath(file_name))

UPF_file_name = only_file
UPF_file = file_path(only_file, only_path, file_name)

print UPF_file_name + "\n"
#gets name of file, and path to the file

UPF_data = file_info_getter(UPF_file)

m_UPF = hashlib.md5(UPF_data)
hash_UPF = m_UPF.hexdigest()
#calculates md5




#adding citation:

file_name = file_name_getter("citation")
citation_file = file_name
cite = file_info_getter(citation_file)


cursor.execute( '''UPDATE pseudos SET upf_name=?, upf=?, md5_upf=?, citation=? WHERE md5_fhi=? ''', (UPF_file_name, UPF_data, hash_UPF, cite, hash,))
#citation and UPF info is added to pseudo table





#optional opts and fill files:

user_choice = raw_input("Would you like to include opts and fill files?\n")

if "y" in user_choice or user_choice == "":

	#opts:
	file_name = file_name_getter("opts")

	only_path, only_file = os.path.split(os.path.normpath(file_name))

	opts_file_name = only_file
	opts_file = file_path(only_file, only_path, file_name)
	#gets name of file, and path to the file

	print "\nopts file name: " + opts_file_name

	opts_data = file_info_getter(opts_file)
	print "The opts file information has been added."
	#opens opts file and grabs everything from it


	#fill:
	file_name = file_name_getter("fill")

        only_path, only_file = os.path.split(os.path.normpath(file_name))

	fill_file_name = only_file
	fill_file = file_path(only_file, only_path, file_name)
	#gets name of file, and path to the file

        print "\nfill file name: " + fill_file_name

        fill_data = file_info_getter(fill_file)
	print "The fill file's information has been added."
        #opens fill file and grabs everything from it


        cursor.execute( '''UPDATE pseudos SET opts_name = ?, opts=?, fill_name=?, fill=? WHERE md5_fhi=? ''', (opts_file_name, opts_data, fill_file_name, fill_data, hash,))
        #fill info and opts info is added to pseudo table
#user decided to include opts and fill files	


elif "n" in user_choice:
	print "opts and fill will not be added."
#user decided not to include opts and fill files
else:
	print "That's not an option."
	sys.exit(1) 






#adding rows into main:

print "\nAdd information to main for the pseudo files given."
user_okay = "ham sandwich"

while user_okay is not "":
	znucl = int(input("What's the znucl/atomic number?\n")) 

	done = False
	while done == False:
		user_semicore = raw_input("Is the semicore True or False?\n") 
		if "t" in user_semicore.lower():
			semicore = "T"
			done = True
		elif "f" in user_semicore.lower():
			semicore = "F"
			done = True
		elif "q" in user_semicore.lower():
			print "User decided to quit."
			sys.exit(1)
		else:
			print "That's not an option. Try again." 
			done = False	

	quality = int(input("What's the quality factor?\n"))

	print "\nZnucl: " + str(znucl)
	print "Semicore: " + semicore
	print "Quality Factor: " + str(quality)
	user_okay = raw_input("Hit enter if this correct: ")
#collects entries for z, qf, and semicore from user and checks them


cursor.execute( ''' INSERT INTO main( z, qf, semicore ) VALUES(?, ?, ?) ''', ( znucl, quality, semicore,))
#adds id, z, qf, and semicore values into main for the new pseudo files

id = cursor.lastrowid
#gets id that was automatically calculated by the database

cursor.execute( ''' UPDATE pseudos SET id=? WHERE md5_fhi=? ''', (id, hash,))
#adds id associated with new entries in main to pseudos so that the pseudo files and info in main is tied


print "The tables main and pseudo have been populated with the new entries."

db.commit()
db.close()
