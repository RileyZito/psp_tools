import os
import sys

original_path = "08_O.out"

number_lines = 0
p_dict = {}
with open(original_path) as start_file:
	searchlines = start_file.readlines()
	for i, line in enumerate(searchlines):
		if line.startswith("!p"):
			p_numbers = line[2:].split()
			p_numbers.pop(1)
			#makes list of p_numbers without !p or p(i) included, just r(i) and V(i)

	#		print p_numbers

			number_V = len(p_numbers) - 1

			p_dict[number_lines] = p_numbers			

			number_lines = number_lines + 1

print p_dict	

number_L = 4 - number_V		


with open("ppot", 'w') as final_file:
	final_file.write("Nr 4\n\n")

	for V in range(1, number_V + 1):
		final_file.write(str(V-1) + "\n")

		for key in p_dict:
			p_num_list = map(lambda x:str(x), p_dict[key])
			final_file.write("r(" + str(key) + ") "),
			final_file.write(p_num_list[0] + " "),
			#radius
			
			for V in range(1, number_V + 1):
				final_file.write("V" + str(V)  + "(" + str(key) + ") "),
				#write down which V it is as well as the index
				final_file.write(p_num_list[V] + " "),
			#Vs for however many there are
	
			final_file.write("\n")
	
	for L in range(1, number_L + 1):
		actual_L = L + V
                final_file.write(str(actual_L-1) + "\n")

		#for key in l_dict:
			#write the r and V's from !L, make sure that you cut off at the number of lines p has or repeat last line if necessary
