import sys, sqlite3, os, bz2, hashlib

db = sqlite3.connect('psps.db')
cursor = db.cursor()


#gets location system of directories will be droped:

print "A system of directories and files with the information of the psps database will be created."

user_location = "ham sandwich"
user_location = raw_input("Where do you want put the directories?")
if user_location == "":
	user_location = os.getcwd()
else:
	while os.path.isdir(user_location) == False:

		print "Invalid path given. Try again."
        	user_location = raw_input("Where do you want to put the system of directories?")
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





def file_creator(type):
	#takes string input of file name like "opts"
	
	type_name = type + "_name"
	cursor.execute( ''' SELECT ''' + type_name + ''' FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))
	#have to connect strings because ? doesn't work for column or table names

	retrieved = cursor.fetchone()[0]
	if retrieved is None:
		print "There is no " + type  + "\n"
		info_location = os.path.join(md5_directory, "info.txt")
                with open(info_location, "a") as info:
                	info.write("\n")
		#for that file, just a line return is entered in info.txt

	else:
        	name = retrieved.encode('ascii', 'ignore')
        	print type + " file name is: " + name

        	cursor.execute( ''' SELECT ''' + type + ''' FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))

        	retrieved = cursor.fetchall()[0]
        	data = str(retrieved[0])
        	#gets file name and text from database and saves it as variables

        	location = os.path.join(md5_directory, name)
        	with open(location, "w") as one_file:
        		one_file.write(data)
        	print name + " was written.\n"
        	#writes found information to a created file with found name
	

		info_location = os.path.join(md5_directory, "info.txt")
		with open(info_location, "a") as info:
			info.write(name + "\n")
		print "info.txt was written.\n"
		#for each file created, that file name is added to info.txt
#to write files if an entry exists in the database





for md5_fhi in md5_fhi_list:
	md5_directory = os.path.join(user_location, md5_fhi)
	os.makedirs(md5_directory)
	#makes a directory with name '[md5 fhi]' using list of fhi md5's

	cursor.execute( ''' SELECT id FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))
	id = cursor.fetchone()[0]
	print "\nid: " + str(id)
	#grabs id using md5 so that id can be used for main table

	#znucl:
	cursor.execute( ''' SELECT z FROM main WHERE id=? ''', (id,))
	z = cursor.fetchone()[0]
	z_location = os.path.join(md5_directory, "znucl")
        with open(z_location, "w") as znucl:
        	znucl.write(str(z))
        print str(z) + " was written to znucl file."

	#quality:
	cursor.execute( ''' SELECT qf FROM main WHERE id=? ''', (id,))
        qf = cursor.fetchone()[0]
        quality_location = os.path.join(md5_directory, "quality")
        with open(quality_location, "w") as quality:
        	quality.write(str(qf))
        print str(qf) + " was written to quality file."

	#semicore:
        cursor.execute( ''' SELECT semicore FROM main WHERE id=? ''', (id,))
        retrieved = cursor.fetchone()[0]
	semicore = retrieved.encode('ascii', 'ignore')
        semicore_location = os.path.join(md5_directory, "semicore")
        with open(semicore_location, "w") as sc:
                sc.write(semicore)
        print semicore + " was written to semicore file.\n"

	#fhi file:
	cursor.execute( ''' SELECT fhi_name FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))
        
	retrieved = cursor.fetchone()[0]
        fhi_name = retrieved.encode('ascii', 'ignore')
	print "fhi file name is: " + fhi_name

	cursor.execute( ''' SELECT fhi FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))

	retrieved = cursor.fetchall()[0]
	fhi_text = str(retrieved[0])
	#gets fhi file name and text from database and saves it as variables

	fhi_location = os.path.join(md5_directory, fhi_name)
        with open(fhi_location, "w") as fhi:
                fhi.write(fhi_text)
        print fhi_name + " was written.\n"
	#writes found fhi information to a created fhi file with found fhi name

	
	#info.txt:
        info_location = os.path.join(md5_directory, "info.txt")
        with open(info_location, "w") as info:
        	info.write(fhi_name + "\n")
	#other files are written in file_creator


	#for other files:

	file_creator("upf")
	file_creator("fill")
	file_creator("opts")


	#citation:
	cursor.execute( ''' SELECT citation FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))
	
	retrieved = cursor.fetchall()[0]
        citation_text = str(retrieved[0])

	citation_location = os.path.join(md5_directory, "citation")
        with open(citation_location, "w") as citation:
                citation.write(citation_text)
        print "Citation was written.\n"
#writes all of the files in each md5_fhi directory




db.close()
