import os
import sys
import sqlite3
import re
import math

original_path = "08_O.out"
other_path = "08_O.dat"
database_name = "suggested_psps.db"





def db_create():
        try:
                open(database_name)
                return False
        #database does exist
        except IOError as e:
                if e.args[0] == 2:
                        user_continue = raw_input("The database doesn't exist. Would you like to [C]reate it "
                                "or [Q]uit?\n")

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
        print "\nDatabase will be created."
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE main'''
                '''(id INTEGER PRIMARY KEY, z INTEGER, qf INTEGER, semicore TEXT)''')

        cursor.execute('''INSERT INTO main(id, semicore ) VALUES(?, ?)''', (0, "don't delete this entry.",))

        cursor.execute('''CREATE TABLE pseudos'''
                '''(id INTEGER, md5_abinet TEXT PRIMARY KEY, abinet_name TEXT, abinet TEXT, md5_upf TEXT, ''' 
		'''upf_name TEXT, upf TEXT, citation TEXT, opts_name TEXT, opts TEXT, fill_name TEXT, fill TEXT)''')
	
	#creates tables
        print "suggested_psps.db tables have been created."
#creates database if it doesn't exist

else:
        db = sqlite3.connect(database_name)
	cursor = db.cursor()
#connects to existing database








number_lines = 0
num_lines = 0
p_dict = {}
L_dict = {}
ecut_list = []
with open(original_path) as start_file:
	searchlines = start_file.readlines()
	for i, line in enumerate(searchlines):
		if line.startswith("!p"):
			p_numbers = line[2:].split()
			p_numbers.pop(1)
			#makes list of p_numbers without !p or p(i) included, just r(i) and V(i)

			number_V = len(p_numbers) - 1

			p_dict[number_lines] = p_numbers			

			number_lines = number_lines + 1
		#makes dictionary of line number with it's radius and V(i)'s for !p
		#!p is for the unique electron levels, aka in O there are 2, the s and p orbital

		if "!L" in line:
			L_numbers = line[3:].split()

			L_dict[num_lines] = L_numbers

			num_lines = num_lines + 1 
		#makes dictionary of line number with it's radius and V(i) for !L
		#!L is for all the non-unique electron levels
		
		if "ecut" in line:
			p = re.compile("ecut\=\d+\.\d+ Ha")
			ecut_string = p.findall(line)[0]
			#gets the string that matches that patten
			ecut_float = float(ecut_string[5:-2])
			#makes a float of the number from the line	
			ecut_number = int(math.ceil(ecut_float))
			#gets int >= float
			ecut_list.append(ecut_number)
		#gets ecut number from line with ecut=# Ha and saves it the rounded up float as an int



#write ppot file:

print "!p r and V's and !L r and V dictionaries were created."	

amount_r = len(p_dict)

dict_index = num_lines - 1 

while len(L_dict) != len(p_dict):
	
	if len(L_dict) > len(p_dict):
		L_dict.pop(dict_index)
		dict_index = dict_index - 1	
	#remove last item from dictionary	
	elif len(L_dict) < len(p_dict):
		last_item = L_dict[dict_index]
		dict_index = dict_index + 1
		L_dict[dict_index] = last_item
		#add last item to dictionary again
print "L_dict was fixed to be the same amount of radii as p_dict"
#make sure that you cut off at the number of lines p has or repeat last line if necessary




number_L = 4 - number_V		


with open("ppot", 'w') as final_file:
	final_file.write(str(amount_r) + " 4\n")

	for V in range(1, number_V + 1):
		final_file.write(str(V-1) + "\n")

		for key in p_dict:
               	        p_num_list = map(lambda x:str(x), p_dict[key])
                        final_file.write(p_num_list[0] + " "),
	                #radius

			final_file.write(p_num_list[V] + " "),
			#write the V for it's orbital, ex: V1 for first orbital, V2 for second orbital

			final_file.write("\n")
	#writes all the !p lines
	
	for L in range(1, number_L + 1):
		actual_L = L + V
                final_file.write(str(actual_L-1) + "\n")

		for key in L_dict:
			L_num_list = map(lambda x:str(x), L_dict[key])
			final_file.write(L_num_list[0] + " "),

			final_file.write(L_num_list[1] + "\n")
			#just write VL not V0, V1
		#write the r and V's from !L, 
	#writes all the !L lines

print "ppot was written with information."





#write quality file:

print("\nList of ecuts in Ha:"),
print ecut_list
ecut = 2*max(ecut_list)
#convert Ha to 
print str(ecut) + " will be written to quality file."

with open("quality", 'w') as quality:
	quality.write(str(ecut))




#for opts and fill files:

core_occupied_list = [0, 0, 0, 0]
valence_occupied_list = [0.0, 0.0, 0.0, 0.0]
rc_list = []

with open(other_path) as dat_file:
        #searchlines = dat_file.readlines()
        for line in dat_file:

		def skipper(next_line):
			while "#" in next_line:
                		#print "skipped"
                		next_line = next(dat_file)
			return next_line

                if "atsym, z, nc, nv, iexc" in line:
			first_info_line = next(dat_file)  
	
			first_info_list = first_info_line.split()						
			#print first_info_list
			z = first_info_list[1]
			nc = int(first_info_list[2])
			nv = int(first_info_list[3])
			iexc = first_info_list[4]
			print "\niexc: " + iexc
			
			next(dat_file)
			next_line = line
			
			next_line = skipper(next_line)
			
			ln = next_line
			for loop in range(1, nc + 1):
				index_for_occupied = int(ln.split()[1])				
				#print index_for_occupied
				core_occupied_list[index_for_occupied] += 1 
				ln = next(dat_file)
				#adds 1 to the orbital specified to know how many electrons occupy that level
			#nc tells how many core electrons there are and l for each tells which orbital it's on 

			for loop in range(1, nv + 1):
				index_for_valence = int(ln.split()[1])
				valence_num = float(ln.split()[2])
				valence_occupied_list[index_for_valence] = valence_num
				#puts in value for valence orbital in valence_occupied_list at the specified orbital
				
				ln = next(dat_file)

			next_line = skipper(ln)
			
			lmax = int(next_line) + 1
			#lmax + 1 is how many lines/rc values there will be			
			
			next_line = next(dat_file)
			ln = skipper(next_line)

			for loop in range(1, lmax + 1):
				rc_val = float(ln.split()[1])			
				rc_list.append(rc_val)
				#gets rc values for all of the lines
				ln = next(dat_file)

			next_line = skipper(next_line)
			
			rc_list.append(float(next_line.split()[2]))
			#grabs the last rc value


print "z: " + z #string
print("Core occupation: "),
print core_occupied_list #ints
print("Valence occupation numbers: "),
print valence_occupied_list #floats

print("Highest rc value: "),
print max(rc_list)
#prints highest rc


#write opts file:

with open("opts", 'w') as opts:
        opts.write(z),
	opts.write("\n"),
	
	for orbital in core_occupied_list:
		opts.write(str(orbital) + " "),

	opts.write("\nscalar\nrel\nlda\n"),
	
	for loop in range(0, 2):
		for orbital in valence_occupied_list:
			opts.write(str(orbital) + " "),
		opts.write("\n"),

print "\nopts file was written with atom configuration."

cursor.execute('''INSERT INTO main(z, qf) VALUES(?, ?)''', (z, ecut,))

#cursor.execute(''INSERT INTO'''



db.commt()
db.close()

