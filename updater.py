import sys, sqlite3, os, hashlib

db = sqlite3.connect('psps.db')
cursor = db.cursor()


#gets location system of directories will be droped:

print "md5 fhi directories will be checked for changes."

user_location = "ham sandwich"
user_location = raw_input("Where is the system of directories?")
if user_location == "":
        user_location = os.getcwd()
else:
        while os.path.isdir(user_location) == False:

                print "Invalid path given. Try again."
                user_location = raw_input("Where is the system of directories? ")
        #checks to make sure the user gave a valid file and doesn't let them continue until they enter a valid one

print user_location





def file_updater(type):
	#takes string input like "opts"
	print "Adding " + type + " file to database."
	#just to see what's what

	if upf_name[-3:] == type.upper():
		type_file = upf_name
	elif opts_name[-4:] == type:
		type_file = opts_name
	elif fill_name[-4:] == type:
		type_file = fill_name
	else:
		print "Something went wrong with file_updater."
		sys.exit(1)
	#for each type of file, it checks to see if [type] == the suffix of [type] + "_name" to know which file to input

	type_name = type + "_name"

	if type_file[0:6] == "blank.":
		print type + " does not exist. It will not be added to the database."
	
	else:
		type_location = os.path.join(user_location, dir_md5, type_file)
		if os.path.isfile(type_location) == True:	
			cursor.execute(''' UPDATE pseudos SET ''' + type_name + '''=? WHERE md5_fhi=? ''', (type_file, hash,))
			#then add that file name to the database
		
			with open(fhi_file, 'r') as file:
				data = file.read()
			#opens file and grabs everything from it
		
			cursor.execute(''' UPDATE pseudos SET ''' + type + '''=? WHERE md5_fhi=? ''', (data, hash,))
			#then add it's info to the database
			

			#if type_file is the upf, its md5 upf needs to be added too.
	
			if type_file == upf_name:
				m_upf = hashlib.md5(data)
				hash_upf = m_upf.hexdigest()
				print "UPF md5: " + hash_upf
				#calculates md5

				cursor.execute(''' UPDATE pseudos SET md5_upf=? WHERE md5_fhi=? ''', (hash_upf, hash,))

		else:
			print "NOTICE: info.txt said file existed but " + type_file + "does not exist in directory."
			print type_file + " will not be added to the database."





#makes list of md5_fhi's:

cursor.execute( ''' SELECT md5_fhi FROM pseudos ''')
one_md5 = cursor.fetchone()
md5_fhi_list = []

while one_md5 is not None:
        md5_fhi_list.append(one_md5[0].encode('ascii', 'ignore'))
        one_md5 = cursor.fetchone()

print "List of current fhi md5's: "
print md5_fhi_list
print "\n"
#grabs all md5's from table. Currently a bit broken because it will add None

dir_md5_fhi_list = os.listdir(user_location)

for dir_md5 in dir_md5_fhi_list:
	if dir_md5 not in md5_fhi_list:
		print "The database does not have " + dir_md5 + " yet."
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
		print "fhi file: " + fhi_name + "\n"
		fhi_file = os.path.join(user_location, dir_md5, fhi_name)

		if os.path.isfile(fhi_file) == True:
			with open(fhi_file, 'r') as file:
			    data = file.read()
			#opens fhi file and grabs everything from it

			m = hashlib.md5(data)
			hash = m.hexdigest()
			print "md5: " + hash
			#calculates md5
		
			if dir_md5 != hash:
				print dir_md5 + " is incorrectly named. The md5 calculation returned a different answer."
                                sys.exit(1)
			#if the directory's md5 didn't match the one calculated from it's fhi file, code ends			

			cursor.execute( ''' SELECT max(id) FROM main ''')

                        current_id = cursor.fetchone()[0]
                        id = current_id + 1
                        #finds last id entered in main and adds one to make a new id

			cursor.execute( ''' INSERT INTO pseudos(id, md5_fhi, fhi_name, fhi) VALUES(?, ?, ?, ?) ''', (id, hash, fhi_name, data,))			
		
			znucl = os.path.join(user_location, dir_md5, "znucl")
			with open(znucl, 'r') as file:
        	                    z = file.read()
			quality = os.path.join(user_location, dir_md5, "quality")
			with open(quality, 'r') as file:
                                    qf = file.read()
			semicore = os.path.join(user_location, dir_md5, "semicore")
			with open(semicore, 'r') as file:
                                    semicore = file.read()

			cursor.execute( ''' INSERT INTO main(id, z, qf, semicore) VALUES(?, ?, ?, ?) ''', (id, z, qf, semicore,))
			#enters z, qf, and semicore info for the id created
			
			file_updater("upf")
			file_updater("opts")
			file_updater("fill")
			#files needed to be added to database too but only if they exist in directory
			
			print "Entries were added to database for " + dir_md5

			#cite:
			citation_file = os.path.join(user_location, dir_md5, "cite")

			with open(citation_file, 'r') as file:
				cite = file.read()
			#opens citation file and grabs everything from it
			
			cursor.execute( '''UPDATE pseudos SET citation=? WHERE md5_fhi=? ''', (cite, hash,))

				
	elif dir_md5 in md5_fhi_list:
		print "Still need to do this.\n"
	#check over everything in dir_md5 and make sure database info is up to date.
	#md5 should be calculated at start to make sure that dir_md5 is correct/the .fhi is correct


db.commit()
db.close()
