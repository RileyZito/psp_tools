import sys, sqlite3, os, bz2, hashlib

db = sqlite3.connect('psps.db')
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




cursor.execute( ''' SELECT fill, opts FROM pseudos WHERE md5_fhi=? ''', (hash,))

retrieved = cursor.fetchall()[0]
print retrieved
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


if raw_fill_db == None or raw_opts_db == None:
	if raw_fill_db == None:
		cursor.execute( ''' UPDATE pseudos SET fill=? WHERE md5_fhi=? ''', (fill_data, hash,))
	else:
		fill_db = raw_fill_db.encode('ascii', 'ignore')
	if raw_opts_db == None:
		cursor.execute( ''' UPDATE pseudos SET opts=? WHERE md5_fhi=? ''', (opts_data, hash,))
	else:
		opts_db = raw_opts_db.encode('ascii', 'ignore')
#if there's no current info for opts and fill, input what was given

else: 
	fill_db = raw_fill_db.encode('ascii', 'ignore')
	opts_db = raw_opts_db.encode('ascii', 'ignore')
	if opts_data == opts_db and fill_data == fill_db:
		#then continue on with opts and fill info 
	
	else:
		print "opts and fill files do not match the current information in the database."
		sys.exit(1)






with open("screen.shells", 'r') as radius_info:
	radius = radius_info.read()
#get radius from screen.shells file in OPF

radius = float(radius.split()[0])

print "radius is " + str(radius)

rounded_radius = round(radius * 100)

radius = rounded_radius/100

print radius
#rounds number from screen.shells to the nearest hundreth 

