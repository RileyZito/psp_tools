import sys, sqlite3, os, bz2, hashlib

db = sqlite3.connect('psps.db')
cursor = db.cursor()




def repeater(file_name):
        file_name_check = raw_input(file_name + "? ")
        if file_name_check != "":
                file_name = raw_input("Re-input file name:")
#gives user a second chance to enter file name in case they mistyped





def file_name_getter(type):
	file_name = ""
	
	while os.path.isfile(file_name) == False:
	
		file_name = raw_input("What's the name of the " + type + " file?")
		repeater(file_name)

        	if os.path.isfile(file_name) == False:
                	print "Invalid file given. Try again."

	return file_name
#checks to make sure the user gave a valid file and doesn't let them continue until they enter a valid one




def file_path_split(only_file, only_path, name):

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





#for fhi:

file_name = file_name_getter(".fhi")

only_path, only_file = os.path.split(os.path.normpath(file_name))

fhi_file_name = only_file
fhi_file = file_path_split(only_file, only_path, file_name)

print fhi_file
print fhi_file_name + "\n"
#gets name of file, and path to the file


with open(fhi_file, 'r') as file:
    data = file.read()
#opens fhi file and grabs everything from it


m = hashlib.md5(data)
hash = m.hexdigest()
print "md5: " + hash
#calculates md5

cursor.execute(''' SELECT md5_fhi FROM pseudos ''')
one_md5 = cursor.fetchone()
md5_list = []

while one_md5 is not None:
	md5_list.append(one_md5[0].encode('ascii', 'ignore'))
	one_md5 = cursor.fetchone()
print "List of current md5's: " 
print md5_list
#grabs all md5's from table. Currently a bit broken because it will add None


m = hashlib.md5(data)
hash = m.hexdigest()
#creates md5 for file

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
UPF_file = file_path_split(only_file, only_path, file_name)

print UPF_file
print UPF_file_name + "\n"
#gets name of file, and path to the file


with open(UPF_file, 'r') as file:
    UPF_data = file.read()
#opens UPF file and grabs everything from it

m_UPF = hashlib.md5(UPF_data)
hash_UPF = m_UPF.hexdigest()
#calculates md5




#adding citation:

file_name = file_name_getter("citation")

citation_file = file_name

with open(citation_file, 'r') as file:
    cite = file.read()
#opens citation file and grabs everything from it


cursor.execute( '''UPDATE pseudos SET upf_name=?, upf=?, md5_upf=?, citation=? WHERE md5_fhi=? ''', (UPF_file_name, UPF_data, hash_UPF, cite, hash,))
#citation and UPF info is added to pseudo table





#optional opts and fill files:

user_choice = raw_input("Would you like to include opts and fill files?")

if "y" in user_choice or user_choice == "":

	#opts:
	file_name = file_name_getter("opts")

	only_path, only_file = os.path.split(os.path.normpath(file_name))

	opts_file_name = only_file
	opts_file = file_path_split(only_file, only_path, file_name)
	#gets name of file, and path to the file

	print "\nopts file name: " + opts_file_name
	print "opts file location: " + opts_file

	with open(opts_file, 'r') as file:
	    opts_data = file.read()
	print "The opts file information has been added."
	#opens opts file and grabs everything from it


	cursor.execute( '''UPDATE pseudos SET opts_name=?, opts=? WHERE md5_fhi=? ''', (opts_file_name, opts_data, hash,))
	#opts info is added to pseudo table


	#fill:
	file_name = file_name_getter("fill")

        only_path, only_file = os.path.split(os.path.normpath(file_name))

	fill_file_name = only_file
	fill_file = file_path_split(only_file, only_path, file_name)
	#gets name of file, and path to the file

        print "\nfill file name: " + fill_file_name
	print "fill file location: " + fill_file

        with open(fill_file, 'r') as file:
            fill_data = file.read()
	print "The fill file's information has been added."
        #opens fill file and grabs everything from it


        cursor.execute( '''UPDATE pseudos SET fill_name=?, fill=? WHERE md5_fhi=? ''', (fill_file_name, fill_data, hash,))
        #fill info is added to pseudo table
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
	znucl = int(input("What's the znucl/atomic number?")) 

	done = False
	while done == False:
		user_semicore = raw_input("Is the semicore True or False?") 
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

	quality = int(input("What's the quality factor?"))

	print "\nZnucl: " + str(znucl)
	print "Semicore: " + semicore
	print "Quality Factor: " + str(quality)
	user_okay = raw_input("Hit enter if this correct: ")
#collects entries for z, qf, and semicore from user and checks them


cursor.execute( ''' SELECT max(id) FROM main ''')

current_id = cursor.fetchone()[0]
calculated_id = current_id + 1
#finds last id entered in main and adds one to make a new id


cursor.execute( ''' INSERT INTO main( id, z, qf, semicore ) VALUES(?, ?, ?, ?) ''', (calculated_id, znucl, quality, semicore,))
#adds id, z, qf, and semicore values into main for the new pseudo files

cursor.execute( ''' UPDATE pseudos SET id=? WHERE md5_fhi=? ''', (calculated_id, hash,))
#adds id associated with new entries in main to pseudos so that the pseudo files and info in main is tied

print "The tables main and pseudo have been populated with the new entries."

db.commit()

db.close()
