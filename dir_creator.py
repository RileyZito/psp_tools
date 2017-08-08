import os
import sys
import sqlite3
import hashlib


def db_check():
        try:
                open('psps.db')
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

if db_check():
        db = sqlite3.connect('psps.db')
        cursor = db.cursor()




#gets location system of directories will be droped:

print "A system of directories and files with the information of the psps database will be created."

user_location = raw_input("Where do you want put the directories?")
if user_location == "":
	user_location = os.getcwd()
else:
	while not os.path.isdir(user_location):
		print "Invalid path given. Try again."
        	user_location = raw_input("Where do you want to put the system of directories?")
	#checks to make sure the user gave a valid file and doesn't let them continue until they enter a valid one

print user_location




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
print "\n"
#grabs all md5's from table





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
        	database_text = str(retrieved[0])
        	#gets file name and text from database and saves it as variables

        	location = os.path.join(md5_directory, name)
        	with open(location, "w") as one_file:
        		one_file.write(database_text)
        	print name + " was written.\n"
        	#writes found information to a created file with found name
	

		info_location = os.path.join(md5_directory, "info.txt")
		with open(info_location, "a") as info:
			info.write(name + "\n")
		print "info.txt was written.\n"
		#for each file created, that file name is added to info.txt
#to write files if an entry exists in the database





def file_creator_main(column_name, name):

	if column_name == "citation":
		cursor.execute('''SELECT citation FROM pseudos WHERE md5_fhi=?''', (md5_fhi,))
                retrieved = cursor.fetchall()[0]
                value = str(retrieved[0])
        	#for citation, fetchall() should be used, and it's grabbed from pseudo table
		print name + " was written.\n"
	#for citation, text is grabbed from pseudos and then written to a file

	else:
		cursor.execute( ''' SELECT ''' + column_name  + ''' FROM main WHERE id=? ''', (id,))
        	retrieved = cursor.fetchone()[0]
		#gets information for column asked for, for the specific id
		if column_name == "semicore":
			value = retrieved.encode('ascii', 'ignore')		
		else:
			value = str(retrieved)
		#for semicore, string needs to be converted, for others, int needs to be changed to a string
		print value + " was written to " + name + " file.\n"
	#gets information for stuff from main and then writes that file
        
	new_file_location = os.path.join(md5_directory, name)
        with open(new_file_location, "w") as new:
                new.write(value)
	#writes info to file
#for znucl, qf, semicore, and cite their files are written





for md5_fhi in md5_fhi_list:
	print "\nmd5_fhi: " + md5_fhi
	md5_directory = os.path.join(user_location, md5_fhi)
	os.makedirs(md5_directory)
	#makes a directory with name '[md5 fhi]' using list of fhi md5's

	cursor.execute( ''' SELECT id FROM pseudos WHERE md5_fhi=? ''', (md5_fhi,))
	id = cursor.fetchone()[0]
	print "id: " + str(id)
	#grabs id using md5 so that id can be used for main table

	#znucl, quality, semicore:
	file_creator_main("z", "znucl")
	file_creator_main("qf", "quality")
	file_creator_main("semicore", "semicore")
        
	#pseudo files:
	file_creator("fhi")
	file_creator("upf")
	file_creator("fill")
	file_creator("opts")


	#citation:
	file_creator_main("citation", "cite")
	
	#info.txt for citation:
	info_location = os.path.join(md5_directory, "info.txt")
        with open(info_location, "a") as info:
                info.write("cite\n")

#writes all of the files in each md5_fhi directory




db.close()
