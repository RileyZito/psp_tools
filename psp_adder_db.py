import os
import sys
import shutil
import fileinput

current_path = os.getcwd()



def repeater(file_path):
        file_name_check = raw_input(file_path + "? ")
        if file_name_check != "":
                file_path = raw_input("Re-input file path or [Q]uit:\n")
                if "q" in file_path.lower():
                        print "User decided to quit."
                        sys.exit(1)
        return file_path
#gives user a second chance to enter file name in case they mistyped




def path_fix(file_path):
	only_path, only_file = os.path.split(os.path.normpath(file_path))

        if only_file == file_path:
                print "The file is in the current directory."
                full_file = os.path.join(current_path, only_file)
        	return [False, only_file]
	#if user only gives a file name and not a path

        else:
                print "The path to the file was given."
                full_file = os.path.join(only_path, only_file)
        	return [True, only_file]
	#if user gives a path to a file
#asks user for file then breaks off the name but keeps the path to the file for reading


print "Check that cite, oncvpsp.x, and adder_db.py are in current directory. All input files will be copied here too."

input_path_list = []

def inputs():
	print "List inputs you would like to convert and add to db. Type stop when finished or [Q]uit to exit."
 	ask = ""
	while "stop" not in ask.lower():
		ask = raw_input("Path to the input file:")
		
		if os.path.isfile(ask):
                	input_path = ask
			input_path = repeater(input_path)

			input_path_list.append(ask)
		
                elif 'q' in ask:
                	print "User decided to quit."
                	sys.exit(1)

		elif "stop" in ask.lower():
                        print "Stopped."

                else:
                        print "That file does not exist. Re-type the file path."
                #allows user to pick as many input files as they want


	print("\nInputs given: "),
	print input_path_list
	return input_path_list
	#requested must be a list of strings


input_path_list = inputs() 
input_list = []

for file_path in input_path_list:
	path_fix = path_fix(file_path)
	fix_path = path_fix[0] #boolean
	file_name = path_fix[1] #string
	input_list.append(file_name)

	if fix_path: 
		new_path = os.path.join(current_directory, file_name) 
		shutil.copy(file_path, new_path)
	#if path was given to a different directory
#makes sure all files are in current directory




for input in input_list:
	print "\nInput: " + input

	#verify:
	def skipper(next_line):
		while "#" in next_line:
                	next_line = next(in_file)
                return next_line

	with open(input) as in_file:
		for line in in_file:
	                if line.startswith("# ATOM AND REFERENCE CONFIGURATION"):
		                first_info_line = skipper(line)

        	                first_info_list = first_info_line.split()
                	        iexc = first_info_list[4]
				psfile = first_info_list[5]
	
        	                #grabs the different values needed and converts them to the type wanted
                	        print "\ncurrent iexc: " + iexc
				print "\ncurrent psfile: " + psfile
				line_number = 11 #might change this later to actually grab line #

				break


	#checks iexc and skips loop if incorrect:
	correct_value = ["-001012", "3", "-001009"]
	if iexc not in correct_value:
		print "\nWARNING!!: iexc was not correct." + input + " will be skipped." 
		continue


	#changes psfile and iexc in input:
	for i, line in enumerate(fileinput.input(input, inplace=1)):
		if line == first_info_line:
			cut_line = '  '.join(first_info_list[:4])
			#cuts off psfile and iexc
			new_line = '  '.join(["    ", cut_line, "3 both\n"])
			sys.stdout.write(new_line)
			#replaces old line with correct line
		else:
			sys.stdout.write(line)
		#to write all other lines

	print "\nCorrected psfile and iexc values in file."
	#fixes file so that it will run correctly


	os.system("./oncvpsp.x < "+ input + " > out")
	print "\nout was created by running oncvpsp.x"
	#runs oncv.x code on input file to get output

	os.system("echo out | ./parser.py") 
	print "\nInformation from out file was converted into files with needed information by running parser.py."
	#runs parser.py code with out as it's input



	#get needed info for adder input:
	with open("znucl") as znucl:
		z = znucl.read()

	with open("semicore") as sc:
		semicore = sc.read()

	with open("quality") as qf:
		quality = qf.read()
	#gets info for main table


	with open("file_names") as names:
		opts_name = names.readline()
		fill_name = names.readline()
		psp8_name = names.readline()
		upf_name = names.readline()
	#gets names of pseudopotential files
	

	#write input file for adder_db.py:
	with open("adder.in", 'w') as adder_input: #adder.in looks like:
		adder_input.write(psp8_name) #symbol.psp8
		adder_input.write("\n")
		adder_input.write(upf_name) #symbol.UPF
		adder_input.write("\n")
		adder_input.write("cite\n") #cite
		adder_input.write("\n")
		adder_input.write("yes\n" + opts_name) #yes and opts	
		adder_input.write("\n")
		adder_input.write(fill_name) #fill
		adder_input.write("\n")
		adder_input.write("yes\n") #yes to ppot
		adder_input.write(z + "\n" + semicore + "\n" + quality + "\n") #z, semicore, quality
		adder_input.write("yes\n") #change this to \n
	
	os.system("python adder_db.py < adder.in")
	#runs adder_db.py with adder.in as it's input

print "\nInputs have been converted and proper information is now stored in database."
#for each input, these steps need to be done: verify, run oncv.x, 






