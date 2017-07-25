import sys, sqlite3, os, bz2, hashlib

db = sqlite3.connect('psp.db')
cursor = db.cursor()


#for fhi:

file_name = ""

while os.path.isfile(file_name) == False:

	file_name = raw_input("What's the name of the .fhi file?")
	
	if os.path.isfile(file_name) == False:
		print "Invalid file given. Try again."	
#checks to make sure the user gave a valid file and doesn't let them continue until they enter a valid one


only_path, only_file = os.path.split(os.path.normpath(file_name))

if only_file == file_name:
        print "The file is in the current directory."
        fhi_path_file = os.getcwd()
        fhi_file_name = only_file
        fhi_file = os.path.join(fhi_path_file, fhi_file_name)
#if user only gives a file name and not a path

else:
        print "The path to the file was given."
        fhi_path_file = only_path
        fhi_file_name = only_file
        fhi_file = os.path.join(fhi_path_file, fhi_file_name)
#if user gives a path to a file

print fhi_file
print file_name + "\n"
#asks user for fhi file then breaks off the name but keeps the path to the file for reading



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

file_name = ""

while os.path.isfile(file_name) == False:

        file_name = raw_input("What's the name of the .UPF file?")

        if os.path.isfile(file_name) == False:
                print "Invalid file given. Try again."
#checks to make sure the user gave a valid file and doesn't let them continue until they enter a valid one



only_path, only_file = os.path.split(os.path.normpath(file_name))

if only_file == file_name:
	print "File in current directory."
	UPF_path_file = os.getcwd()
	UPF_file_name = only_file
	UPF_file = os.path.join(UPF_path_file, UPF_file_name)
#if user gives only a file name

else:
	print "Path to a file was given."
	UPF_path_file = only_path
        UPF_file_name = only_file
        UPF_file = os.path.join(UPF_path_file, UPF_file_name)
#if user gives a path to a file

print UPF_file
print UPF_file_name + "\n"


with open(UPF_file, 'r') as file:
    data = file.read()
#opens UPF file and grabs everything from it

cursor.execute( '''UPDATE pseudos SET upf_name=?, upf=? WHERE md5_fhi=? ''', (UPF_file_name, data, hash,))




db.commit()

db.close()
