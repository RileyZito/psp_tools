#!/usr/bin/python2

import os
import sys
import re
import math

rc_edit = .5
#added to rc

out_path = raw_input("What's the name of the out file?")
#file where information will be grabbed from

if not os.path.isfile(out_path):
	sys.exit(1)       





element_names = {
        1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F",
        10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K",
        20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
        30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y",
        40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "Zr",
        50: "Sn", 51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr",
        60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm",
        70: "Yb", 71: "Lu", 72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au",
        80: "Hg", 81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac",
        90: "Th", 91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es",
        100: "Fm", 101: "Md", 102: "No", 103: "Lr"
}
#list of atomic numbers with their corresponding symbol




number_lines = 0
num_lines = 0
p_dict = {}
L_dict = {}
ecut_list = []
with open(out_path) as out_file:
	searchlines = out_file.readlines()
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
#orbitals that aren't occupied = number_L, in this case just act like there's a max of 4 orbitals

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

print "ppot was written."



#write quality file:

print("\nList of ecuts in Ha:"),
print ecut_list
ecut = 2*max(ecut_list)
#convert Ha to 
print str(ecut) + " will be written to quality file."

with open("quality", 'w') as quality:
	quality.write(str(ecut))






#information for opts and fill files:

core_occupied_list = [0, 0, 0, 0]
valence_occupied_list = [0.0, 0.0, 0.0, 0.0]
semicore_decider_list = []
rc_list = []

with open(out_path) as out_file:
	def skipper(next_line):
		while "#" in next_line:
        		next_line = next(out_file)
        	return next_line


        for line in out_file:
                if line.startswith("# ATOM AND REFERENCE CONFIGURATION"):
			first_info_line = skipper(line)  

			first_info_list = first_info_line.split()						
			#print first_info_list
			z = str(int(float(first_info_list[1])))
			nc = int(first_info_list[2])
			nv = int(first_info_list[3])
			iexc = first_info_list[4]
			#grabs the different values needed and converts them to the type wanted
			print "\niexc: " + iexc
		
			next(out_file)
			next_line = line
			
			next_line = skipper(next_line)
			ln = next_line

			for loop in range(1, nc + 1):
				index_for_occupied = int(ln.split()[1])				
				#print index_for_occupied
				core_occupied_list[index_for_occupied] += 1 
				ln = next(out_file)
			#adds 1 to the orbital specified to know how many electrons occupy that level
			#nc tells how many core electrons there are and l for each tells which orbital it's on 

			for loop in range(1, nv + 1):
				index_for_valence = int(ln.split()[1])
				semicore_decider_list.append(index_for_valence)
				valence_num = float(ln.split()[2])
				valence_occupied_list[index_for_valence] = valence_num
				#puts in value for valence orbital in valence_occupied_list at the specified orbital
				
				ln = next(out_file)

			next_line = skipper(ln)
		
			lmax = int(next_line) + 1
			#lmax + 1 is how many lines/rc values there will be			
			
			next_line = next(out_file)
			ln = skipper(next_line)

			for loop in range(1, lmax + 1):
				rc_val = float(ln.split()[1])			
				rc_list.append(rc_val)
				#gets rc values for all of the lines
				ln = next(out_file)
	
			next_line = skipper(next_line)
				
			rc_list.append(float(next_line.split()[2]))
			#grabs the last rc value
			
			break
			#this info is repeated 3 times, it's only needed once

print "z: " + z #string

symbol = element_names[int(z)]
print symbol
print "!!!!!!"
#for later file naming
	
print("Core occupation: "),
print core_occupied_list #ints
	
print("Valence occupation numbers: "),
print valence_occupied_list #floats

print("Highest rc value: "),
rc = max(rc_list)
print rc
#prints highest rc




if len(semicore_decider_list) == len(set(semicore_decider_list)):
	semicore = "F"
	#no duplicates
else:
	semicore = "T"
#set gets rid of duplicate items. If one of the l's is repeated for valence, then there is semicore


quality = ecut

main_dict = {1: int(z), 2: semicore, 3: quality} #quality and z are ints, semicore is a string
#just in case

with open("znucl", 'w') as znucl:
        znucl.write(z)

with open("semicore", 'w') as sc:
        sc.write(semicore)
#writes semicore and znucl files




opts_name = symbol.lower() + ".opts"
fill_name = symbol.lower() + ".fill"

#write opts file:
	
with open(opts_name, 'w') as opts:
        opts.write(z),
	opts.write("\n"),
	
	for orbital in core_occupied_list:
		opts.write(str(orbital) + " "),

	opts.write("\nscalar\nrel\nlda\n"),
	
	for loop in range(0, 2):
		for orbital in valence_occupied_list:
			opts.write(str(orbital) + " "),
		opts.write("\n"),

print "\nopts file was written."



#writes fill file:

with open(fill_name, 'w') as fill:
        radius = str(rc + rc_edit)
	
	fill.write("2\n"),
	fill.write("0.20 3.00 0.0001\n"),
	fill.write(radius),
	fill.write("\n0.05 20."),

print "\nfill file was written."






#information for psp8 and UPF files:

psp8_text_list = []
upf_text_list = []

with open(out_path) as out_file:
	for line in out_file:
		if line.strip() == "Begin PSPCODE8":
			break
    		#reads text from pspcode8 on

	for line in out_file:
		if line.strip() == 'END_PSP':
                        break
	        #stops when it sees end_psp

		else:
			psp8_text_list.append(line)
        	#grabs all lines before it sees end_psp
	#gets text for psp8
	
	for line in out_file:
		if line.strip() == "Begin PSP_UPF":
                        break
                #reads text from psp_upf on

        for line in out_file:
                if line.strip() == 'END_PSP':
                        break
                #stops when it sees end_psp

                else:
                        upf_text_list.append(line)
                #grabs all lines before it sees end_psp
	#gets text for upf




psp8_name = symbol.lower() + ".psp8"
upf_name = symbol.lower() + ".UPF"

#writes psp8:

with open(psp8_name, 'w') as psp8:
	for line in psp8_text_list:
		psp8.write(line)

print "\npsp8 was written."
#writes psp8 file with text from out




#writes upf:

with open(upf_name, 'w') as upf:
        for line in upf_text_list:
                upf.write(line)

print "\nUPF was written."
#writes upf file with text from out




#other necessary files:
with open("file_names", 'w') as names:
	names.write(opts_name + "\n")
	names.write(fill_name + "\n")
	names.write(psp8_name + "\n")
	names.write(upf_name + "\n")

