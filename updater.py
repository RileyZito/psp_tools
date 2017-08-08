import os
import sys
import sqlite3
import hashlib


database_name = 'psps.db'

def db_create():
        try:
                open(database_name)
                return False
        #database does exist
        except IOError as e:
                if e.args[0] == 2:
                        user_continue = raw_input("The database doesn't exist. Would you like to [C]reate it or [Q]uit?")
                        if "q" in user_continue.lower():
                                print "User decided to quit."
                                sys.exit(1)
                        elif "c" in user_continue.lower():
                                return True

                #if database doesn't exist, warn user and create it 
                else:
                        print e
                        sys.exit(1)

if db_create():
        print "Database will be created."
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
       
	cursor.execute('''CREATE TABLE main(id INTEGER PRIMARY KEY, z INTEGER, qf INTEGER, semicore TEXT)''') 
	
	cursor.execute('''INSERT INTO main(id, semicore ) VALUES(?, ?)''', (0, "don't delete this entry.",))
       
	cursor.execute('''CREATE TABLE pseudos'''
		'''(id INTEGER, md5_fhi TEXT PRIMARY KEY, fhi_name TEXT, fhi TEXT, md5_upf TEXT, upf_name TEXT, upf TEXT, ''' 
		'''citation TEXT, opts_name TEXT, opts TEXT, fill_name TEXT, fill TEXT) ''' )
        
	cursor.execute('''CREATE TABLE core_potential'''
		'''(id INTEGER PRIMARY KEY, md5_fhi TEXT, N INTEGER, L INTEGER, vc_bare TEXT, vpseud1 TEXT, vvallel TEXT) ''')
        
	cursor.execute(''' INSERT INTO core_potential( id, vc_bare) VALUES(?, ?)''', (0, "don't delete this entry.",))
        
	cursor.execute(''' CREATE TABLE radii_info( id INTEGER, radius REAL, text_file TEXT ) ''')
        
        print "psps.db tables have been created."
#creates database if it doesn't exist

else:
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
#connects to existing database





#gets location system of directories will be droped:

print "md5 fhi directories will be checked for changes."

user_location = raw_input("Where is the system of directories?")
if user_location == "":
        user_location = os.getcwd()
else:
        while os.path.isdir(user_location) == False:

                print "Invalid path given. Try again."
                user_location = raw_input("Where is the system of directories? ")
        #checks to make sure the user gave a valid file and doesn't let them continue until they enter a valid one

print user_location




def file_info_getter(full_file):
	with open(full_file, 'r') as file_info:
		data = file_info.read()
	return data



def file_updater(type):
	#takes string input like "opts"
	print "\nAdding " + type + " file to database."
	#just to see what's what

	if upf_name.endswith(type.upper()):
		type_file = upf_name
	elif opts_name.endswith(type):
		type_file = opts_name
	elif fill_name.endswith(type):
		type_file = fill_name
	else:
		print "Something went wrong with file_updater."
		sys.exit(1)
	#for each type of file, it checks to see if [type] == the suffix of [type] + "_name" to know which file to input

	type_name = type + "_name"

	if type_file.startswith("blank."):
		print type + " does not exist. It will not be added to the database."
	
	else:
		type_location = os.path.join(user_location, dir_md5, type_file)
		if os.path.isfile(type_location):	
			cursor.execute(''' UPDATE pseudos SET ''' + type_name + '''=? WHERE md5_fhi=? ''', (type_file, hash,))
			#then add that file name to the database
		
			data = file_info_getter(type_location)
			#opens file and grabs everything from it
		
			cursor.execute(''' UPDATE pseudos SET ''' + type + '''=? WHERE md5_fhi=? ''', (data, hash,))
			#then add it's info to the database
			

			#if type_file is the upf, its md5 upf needs to be added too.
	
			if type_file == upf_name:
				data_upf = file_info_getter(type_location)

				m_upf = hashlib.md5(data_upf)
				hash_upf = m_upf.hexdigest()
				print "UPF md5: " + hash_upf
				#calculates upf md5

				cursor.execute(''' UPDATE pseudos SET md5_upf=? WHERE md5_fhi=? ''', (hash_upf, hash,))

		else:
			print "NOTICE: info.txt said file existed but " + type_file + "does not exist in directory."
			print type_file + " will not be added to the database."
#to add new files to database






def file_name_checker(type):
	type_name = type + "_name"
        print "\n" + type_name 	

	if upf_name.endswith(type.upper()):
                file_name = upf_name
        elif opts_name.endswith(type):
                file_name = opts_name
        elif fill_name.endswith(type):
                file_name = fill_name
        else:
                print "Something went wrong with file_name_checker."
                sys.exit(1)
        #to figure out which type got entered and then get that file name
	
	print "File name: " + file_name

	if file_name.startswith("blank."):
                print type + " does not exist. The database won't be checked."

        else:

		cursor.execute( ''' SELECT ''' + type_name + ''' FROM pseudos WHERE md5_fhi=?''', (hash,))
		retrieved = cursor.fetchone()[0]
		database_type_name = retrieved.encode('ascii', 'ignore') 
		#gets name listed for file in database


		if file_name != database_type_name:
			cursor.execute( ''' UPDATE pseudos SET ''' + type_name + '''=? WHERE md5_fhi=? ''', (file_name, hash,))
			print "Database was updated with new " + type + " name."
		#if name found in info.txt doesn't match name in database, write new name to database

#checks that file name in database is up to date





def file_checker(type):
	print "\n" + type
	if upf_name.endswith(type.upper()):
                type_file_name = upf_name
        elif opts_name.endswith(type):
                type_file_name = opts_name
        elif fill_name.endswith(type):
                type_file_name = fill_name
        elif "citation" == type:
                type_file_name = citation_name
        else:
                print "Something went wrong with file_checker."
                sys.exit(1)
	
	print "File name: " + type_file_name

        if type_file_name.startswith("blank."):
                print type + " does not exist. The database won't be checked."

        else:
		cursor.execute( ''' SELECT ''' + type + ''' FROM pseudos WHERE md5_fhi=?''', (hash,))
		retrieved = cursor.fetchall()[0]	
		database_text = retrieved[0]
		#gets text for type from database
 	

		type_file = os.path.join(user_location, dir_md5, type_file_name)
		print type_file
        	file_text = file_info_getter(type_file) 		

		if str(file_text) != database_text:
			cursor.execute( ''' UPDATE pseudos SET ''' + type + '''=? WHERE md5_fhi=? ''', (file_text, hash,))
			print "Database was updated with new " + type + " information."
		#compares text from database to text in file from directory, updates database with changes
		
			if type_file_name == upf_name:
				m_UPF = hashlib.md5(file_text)
                        	hash_UPF = m_UPF.hexdigest()
                        	print "md5 UPF: " + hash_UPF
 				cursor.execute( ''' UPDATE pseudos SET md5_upf=? WHERE md5_fhi=? ''', (hash_UPF, hash,))
                        #calculates new md5 for UPF file
#checks a file to see if it's up to date compared to the database





#makes list of md5_fhi's:

cursor.execute( ''' SELECT md5_fhi FROM pseudos ''')
md5_raw_list = cursor.fetchall()
md5_fhi_list = []

for one_md5 in md5_raw_list:
        if one_md5[0] != None:
                md5 = one_md5[0].encode('ascii', 'ignore')
                md5_fhi_list.append(md5)

print "List of current md5's: "
print md5_fhi_list
print "\n\n"
#grabs all md5's from table


dir_md5_fhi_list = os.listdir(user_location)

for dir_md5 in dir_md5_fhi_list:

	if dir_md5 not in md5_fhi_list:
		print "NOT IN DATABASE: " + dir_md5 + "\nDatabase will be populated with new entry."
		info_file = os.path.join(user_location, dir_md5, "info.txt")
		with open(info_file, "r") as info:
			searchlines = info.readlines()
			for i, line in enumerate(searchlines):
				if ".fhi" in line:
					for l in searchlines[0:i]: fhi_name = l.split()[0]
					for l in searchlines[i:i+1]: 
						if l == "\n":
							upf_name = "blank.upf"
						else:
							upf_name = l.split()[0]
					for l in searchlines[i+1:i+2]: 
                                                if l == "\n":
                                                        opts_name = "blank.opts"
                                                else:
                                                        opts_name = l.split()[0]
					for l in searchlines[i+2:i+3]:  
                                                if l == "\n":
                                                        fill_name = "blank.fill"
                                                else:
                                                        fill_name = l.split()[0]					
		#goes through info.txt file and grabs names of different files. if file isn't there it sets file = ""

		#populating database:
		print "\nfhi file: " + fhi_name
		fhi_file = os.path.join(user_location, dir_md5, fhi_name)

		if os.path.isfile(fhi_file):
			data = file_info_getter(fhi_file)
			#opens fhi file and grabs everything from it

			m = hashlib.md5(data)
			hash = m.hexdigest()
			print "md5: " + hash
			#calculates md5
		
			if dir_md5 != hash:
				print dir_md5 + " is incorrectly named. The md5 calculation returned a different answer."
                                sys.exit(1)
			#if the directory's md5 didn't match the one calculated from it's fhi file, code ends			


			znucl = os.path.join(user_location, dir_md5, "znucl")
                        z = file_info_getter(znucl)
                        quality = os.path.join(user_location, dir_md5, "quality")
                        qf = file_info_getter(quality)
                        semicore = os.path.join(user_location, dir_md5, "semicore")
                        semicore = file_info_getter(semicore)

                        cursor.execute('''INSERT INTO main(z, qf, semicore) VALUES(?, ?, ?)''', (z, qf, semicore,))
                        #enters z, qf, and semicore info for the id created			
			
			print "\nznucl " + z + ", semicore " + semicore + ", and quality " + qf + " were entered."

			id = cursor.lastrowid

			cursor.execute('''INSERT INTO pseudos(id, md5_fhi, fhi_name, fhi) VALUES(?, ?, ?, ?) ''', 
				(id, hash, fhi_name, data,))			
			

			file_updater("upf")
			file_updater("opts")
			file_updater("fill")
			#files needed to be added to database too but only if they exist in directory
			
			print "\nEntries were added to database for " + dir_md5

			#cite:
			citation_file = os.path.join(user_location, dir_md5, "cite")
			cite = file_info_getter(citation_file)
			#opens citation file and grabs everything from it
			
			cursor.execute( '''UPDATE pseudos SET citation=? WHERE md5_fhi=? ''', (cite, hash,))
			print "\n"
	#if md5 fhi wasn't in database
	
				

	elif dir_md5 in md5_fhi_list:
		print "ALREADY IN DATABASE: " + dir_md5 + "\nDirectory will be checked for updates.\n"
		
		info_file = os.path.join(user_location, dir_md5, "info.txt")
                with open(info_file, "r") as info:
                        searchlines = info.readlines()
                        for i, line in enumerate(searchlines):
                                if ".fhi" in line:
                                        for l in searchlines[0:i]: fhi_name = l.split()[0]
                                        for l in searchlines[i:i+1]:
                                                if l == "\n":
                                                        upf_name = "blank.upf"
                                                else:
                                                        upf_name = l.split()[0]
					for l in searchlines[i+1:i+2]:
                                                if l == "\n":
                                                        opts_name = "blank.opts"
                                                else:
                                                        opts_name = l.split()[0]
                                        for l in searchlines[i+2:i+3]:
                                                if l == "\n":
                                                        fill_name = "blank.fill"
                                                else:
                                                        fill_name = l.split()[0]
					for l in searchlines[i+3:i+4]:
                                                if l == "\n":
                                                        citation_name = "blank.fill"
                                                else:
                                                        citation_name = l.split()[0]
                #goes through info.txt file and grabs names of different files. if file isn't there it sets file = ""

					
		print "fhi file: " + fhi_name
                fhi_file = os.path.join(user_location, dir_md5, fhi_name)

                if os.path.isfile(fhi_file):
                        data = file_info_getter(fhi_file)
                        #opens fhi file and grabs everything from it

                        m = hashlib.md5(data)
                        hash = m.hexdigest()
                        print "md5: " + hash
                        #calculates md5


			if dir_md5 != hash:
                		print dir_md5 + " is incorrectly named. The md5 calculation returned a different answer."
                		sys.exit(1)
                	#if the directory's md5 didn't match the one calculated from it's fhi file, code ends     
		else:
			print "the fhi file does not exist."
			sys.exit(1)

		file_name_checker("upf")
		file_checker("upf")
	
		file_name_checker("opts")
		file_checker("opts")

		file_name_checker("fill")
		file_checker("fill")

		file_checker("citation")
		#checks that info and names in database are up to date and updates database if needed		

		cursor.execute( ''' SELECT id FROM pseudos WHERE md5_fhi=?''', (hash,))

                id = cursor.fetchone()[0]
		#gets id from pseudos so it knows what id to check in main

		def main_update(id, name, database_name):
			file_location = os.path.join(user_location, dir_md5, name)
			main_file_info = file_info_getter(file_location)
			
			cursor.execute('''SELECT ''' + database_name + ''' FROM main WHERE id=?''', (id,)) 
			retrieved = cursor.fetchone()

			if name == "znucl" or name == "quality":
				main_database_info = str(retrieved[0])
			elif name == "semicore":
				main_database_info = retrieved[0].encode('ascii', 'ignore')
			
			print "\n" + name + " from file: " + main_file_info
	                print name + " from database: " + main_database_info
 
        	        if main_file_info != main_database_info:
                	        cursor.execute( ''' UPDATE main SET ''' + database_name + '''=? WHERE id=? ''', 
					(main_file_info, id,))
           
                	        print name + " was updated in database."
		

		main_update(id, "znucl", "z")
		main_update(id, "semicore", "semicore")
		main_update(id, "quality", "qf")
		#z, qf, and semicore- make sure info in those files matches up with info in main
	print "\n"
	#if md5 fhi was in database, check over everything in dir_md5 and make sure database info is up to date.




db.commit()
db.close()
