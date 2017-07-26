import sys, sqlite3, os, hashlib, glob

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
		fhi_file = os.path.join(user_location, dir_md5, *.fhi)
		only_path, fhi_name = os.path.split(os.path.normpath(fhi_file))

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
		
			with open("znucl", 'r') as file:
        	                    z = file.read()
			with open("quality", 'r') as file:
                                    qf = file.read()
			with open("semicore", 'r') as file:
                                    semicore = file.read()

			cursor.execute( ''' INSERT main(id, z, qf, semicore) VALUES(?, ?, ?, ?) ''', (id, z, qf, semicore,))
			#enters z, qf, and semicore info for the id created
			
			#files needed to be added to database too

	elif dir_md5 in md5_fhi_list:
		print "Still need to do this."
	#check over everything in dir_md5 and make sure database info is up to date.
	#md5 should be calculated at start to make sure that dir_md5 is correct/the .fhi is correct

db.commit()
db.close()
