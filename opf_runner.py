import sys, sqlite3, os, bz2, hashlib

db = sqlite3.connect('../psps.db')
cursor = db.cursor()

current_directory = os.getcwd()



def repeater(file_name):
        file_name_check = raw_input(file_name + "? ")
        if file_name_check != "":
                file_name = raw_input("Re-input file name:")
	return file_name
#gives user a second chance to enter file name in case they mistyped




def file_name_getter(type):
        file_name = ""

        while os.path.isfile(file_name) == False:

                file_name = raw_input("What's the name of the " + type + " file?")
                file_name = repeater(file_name)

                if os.path.isfile(file_name) == False:
                        print "Invalid file given. Try again."

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




print "Make sure you are in the OPF directory."

file_name = file_name_getter(".fhi")

only_path, only_file = os.path.split(os.path.normpath(file_name))
fhi_file = only_file

with open(fhi_file, 'r') as fhi_info:
    data = fhi_info.read()
#opens fhi file and gets everything from it

md5_list = []
m = hashlib.md5(data)
hash = m.hexdigest()
print "md5: "
print hash
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


if hash not in md5_list:
        print "\nmd5 fhi is not in pseudo table. Use adder_db to add this entry."
        sys.exit(1)
#if md5 doesn't exist, stop code





def fill_opts_check():
	if raw_fill_db == None and raw_opts_db == None:
	        cursor.execute( ''' UPDATE pseudos SET fill=?, opts=? WHERE md5_fhi=? ''', (fill_data, opts_data, hash,))
	#if neither opts or fill is in the databse, the database is updated with both
	elif raw_fill_db == None or raw_opts_db == None:
        	if raw_fill_db == None:
        	        cursor.execute( ''' UPDATE pseudos SET fill=? WHERE md5_fhi=? ''', (fill_data, hash,))
        	#if fill isn't in database, new fill info is added to database
        	else:
        	        fill_db = raw_fill_db.encode('ascii', 'ignore')
        	        if fill_data != fill_db:
        	                print "The fill information does not match the current information in the database."
                	        sys.exit(1)
        	#if fill is in database, new fill info must match
        	if raw_opts_db == None:
                	cursor.execute( ''' UPDATE pseudos SET opts=? WHERE md5_fhi=? ''', (opts_data, hash,))
        	#if opts isn't in database, new opts info is added to database
        	else:
                	opts_db = raw_opts_db.encode('ascii', 'ignore')
                	if opts_data != opts_db:
                	        print "The opts information does not match the current information in the database."
                	        sys.exit(1)
	#if there's no current info for opts or fill, input what was given

	else:
        	fill_db = raw_fill_db.encode('ascii', 'ignore')
        	opts_db = raw_opts_db.encode('ascii', 'ignore')
        	if opts_data == opts_db and fill_data == fill_db:
        	        print "The opts and fill information is correct."
        	        #then continue on with opts and fill info 

        	else:
        	        print "opts and fill files do not match the current information in the database."
                	sys.exit(1)
#checks and updates fill and opts info in database




cursor.execute( ''' SELECT fill, opts FROM pseudos WHERE md5_fhi=? ''', (hash,))

retrieved = cursor.fetchall()[0]
raw_fill_db = retrieved[0]
raw_opts_db = retrieved[1]
#retrieves opts and fill info from database

file_name = file_name_getter(".fill")

only_path, only_file = os.path.split(os.path.normpath(file_name))
fill_file = only_file
full_fill_file = file_path(only_file, only_path, file_name)
fill_data = file_info_getter(full_fill_file)

file_name = file_name_getter(".opts")

only_path, only_file = os.path.split(os.path.normpath(file_name))
opts_file = only_file
full_opts_file = file_path(only_file, only_path, file_name)
opts_data = file_info_getter(full_opts_file)
#gets opts and fill info from files

fill_opts_check()
cursor.execute( ''' SELECT fill, opts FROM pseudos WHERE md5_fhi=? ''', (hash,))
retrieved = cursor.fetchall()[0]
fill = retrieved[0].encode('ascii', 'ignore')
opts = retrieved[1].encode('ascii', 'ignore')

print fill
print opts
#retrieves updated/checked opts and fill info from database



#for md5 in md5_list:
#	cursor.execute( ''' SELECT max(id) FROM core_potential ''' )

#	retrieved = cursor.fetchall()[0]
#	id = retrieved[0]
#	id = int(id) + 1
#	print "new id: " + str(id)
#
#	cursor.execute( '''INSERT INTO core_potential( id, md5_fhi ) VALUES(?, ?) ''', (id, md5,))

#	cursor.execute( '''SELECT * FROM core_potential ''' )
#	print cursor.fetchall()
	
#	cursor.execute( '''INSERT INTO radii_info( id ) VALUES(?) ''', (id, ))
#adds each md5_fhi to the database (I'll change it to update but for now)




with open("screen.shells", 'r') as radius_info:
	radius = radius_info.read()
#get radius from screen.shells file in OPF

radius = float(radius.split()[0])

rounded_radius = round(radius * 100)

radius = rounded_radius/100

print "radius is " + str(radius)

#rounds number from screen.shells to the nearest hundreth 


cursor.execute( '''SELECT id FROM core_potential WHERE md5_fhi=?''', (hash,))
id = cursor.fetchone()[0]
print id
cursor.execute( '''UPDATE radii_info SET radius=? WHERE id=? ''', (radius, id,)) 
#inputs radius to radii_info table for this md5


with open("edges", 'r') as edges:
	numbers = edges.read()

list_numbers = numbers.split()
print list_numbers

N = int(list_numbers[1])
L = int(list_numbers[2])

#print N
#print L
cursor.execute( '''UPDATE core_potential SET N=?, L=? WHERE id=? ''', (N, L, id,))


with open("znucl", 'r') as znucl:
	z = znucl.read()

z = int(z.split()[0])
#print z


edgename = "z%03in%02il%02i" % (z, N, L)

#print edgename
possible_files = []
list_files = os.listdir("zpawinfo")

for one_file in list_files:
	if one_file.endswith(edgename):
		possible_files.append(one_file)
	
for possible_file in possible_files:
	if possible_file.startswith("vc_bare"):
		print possible_file
		vc_bare = os.path.join("zpawinfo", possible_file)
	elif possible_file.startswith("vpseud1"):
		print possible_file
		vpseud1 = os.path.join("zpawinfo", possible_file)
	elif possible_file.startswith("vvallel"):
		print possible_file
		vvallel = os.path.join("zpawinfo", possible_file)

with open(vc_bare, 'r') as bare:
	vc_bare_text = bare.read()	

with open(vpseud1, 'r') as pseud:
	vpseud1_text = pseud.read()

with open(vvallel, 'r') as vallel:
	vvallel_text = vallel.read()

cursor.execute( '''UPDATE core_potential SET vc_bare=?, vpseud1=?, vvallel=? WHERE id=? ''', (vc_bare_text, vpseud1_text, vvallel_text, id,))

temp = "R%f" % radius
ending = temp[:-4]

for one_file in list_files:
	if one_file.startswith("vc_bare") and one_file.endswith(ending):
		print one_file
		text_file = os.path.join("zpawinfo", one_file)

with open(text_file, 'r') as text:
        data_text_file = text.read()

cursor.execute( '''UPDATE radii_info SET text_file=? WHERE id=? ''', (data_text_file, id,))


db.commit()
db.close()
