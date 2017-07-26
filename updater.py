import sys, sqlite3, os, bz2, hashlib

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

