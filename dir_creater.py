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

for md5_fhi in md5_fhi_list:
	md5_directory = os.path.join(user_location, md5_fhi)
	os.makedirs(md5_directory)
	#makes a directory with name '[md5 fhi]' using list of fhi md5's

	cursor.execute( ''' SELECT id FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))
	id = cursor.fetchone()[0]
	print "id: " + str(id)
	#grabs id using md5 so that id can be used for main table

	#znucl:
	cursor.execute( ''' SELECT z FROM main WHERE id=? ''', (id,))
	z = cursor.fetchone()[0]
	z_location = os.path.join(md5_directory, "znucl")
        with open(z_location, "w") as znucl:
        	znucl.write(str(z))
        print "znucl file for " + str(z) + " was written.\n"

	#quality:
	cursor.execute( ''' SELECT qf FROM main WHERE id=? ''', (id,))
        qf = cursor.fetchone()[0]
        quality_location = os.path.join(md5_directory, "quality")
        with open(quality_location, "w") as quality:
        	quality.write(str(qf))
        print "quality file for " + str(qf) + " was written.\n"

	#semicore:




db.close()
