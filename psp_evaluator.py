import os
import sys
import sqlite3
import xml.etree.ElementTree as ET


database_name = 'psps.db'

def db_check():
        try:
                open(database_name)
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

if db_check() == True:
        db = sqlite3.connect(database_name)
        cursor = db.cursor()

cursor.execute('''DROP TABLE IF EXISTS Kpoint_eigenvals''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Kpoint_eigenvals'''
	'''(id INTEGER PRIMARY KEY, Kpoint TEXT, Kpoint_info TEXT, eigenval_text TEXT, avg_shift REAL)''')

#only continues if database exists. Then drops Kpoint_eigenvals table if it exists, and creates it either way for use




tree = ET.parse('DFT/Out/system.save/data-file.xml') #data-file.xml or k00001/eigenval.xml
root = tree.getroot()

#for child in root:
#       print child.tag, child.attrib


#print root[11].tag
brillouin_zone = root[11]
#Brillouin Zone


number_kpoint_title = brillouin_zone[0]
number_kpoint = int(number_kpoint_title.text)
#how many kpoints there are


loops = number_kpoint + 4

#for kpoint in brillouin_zone[4:loops]:
#        print kpoint.tag, ':', kpoint.attrib
#all of the kpoints in data-file.xml





kpoint_dict = {}

for number in range(1, number_kpoint + 1):
	num = str(number)
	digits = len(num) 
	#how many digits the number has
	index = (digits - 1)*(-1)

	if index < 0:
		k_string = "K0000"[:index]
	#if double digit remove one zero and add number, if thriple digit number remove two zeroes and add number, etc
	elif index == 0: 
		k_string = "K0000"
	#can't take the index 0 of k_string, only works when u can take 1 or more zeros off the end of k_string

	kpoint = k_string + num 
	kpoint_dict[number] = kpoint
#prints all of the different kpoints so I know which directories exist to get their eigenvals




kpoint_eigenval_db_dict = {}

for key in kpoint_dict:
	kpoint = kpoint_dict[key]
	#print(key),
	#print kpoint

	eigenval_path = os.path.join("DFT/Out/system.save", kpoint, "eigenval.xml")
	tree = ET.parse(eigenval_path)
	root = tree.getroot()

	#print root[2].tag
	eigenvals = root[2].text
	#eigenvals

	
	loop = 3 + number
	#which kpoint is which
	kpoint_info = str(brillouin_zone[loop].attrib)
	#the info for a kpoints in data-file.xml


	cursor.execute('''INSERT INTO Kpoint_eigenvals(id, Kpoint, Kpoint_info, eigenval_text) VALUES(?, ?, ?, ?)''', 
		(key, kpoint, kpoint_info, eigenvals,))

	#print kpoint + " information was added to Kpoint_eigenvals table."
	#adds each of the kpoint stuff to the database

	eigenval_db_dict = {}
	n = 0
	for eigenval in eigenvals.split():
		n = n + 1
		eigenval_db_dict[n] = float(eigenval)	
	#dict of a kpoint's eigenvals
	
	kpoint_eigenval_db_dict[key] = eigenval_db_dict
	#dict of kpoint: eigenvals

print "Information was added to Kpoint_eigenvals table."

number_eigenvalues = n




ae_path = "/flash/maz2/diamond.ae/EIGVAL.OUT"
#qe_path = "DFT/Out/system.save/charge-density.dat"

kpoint_eigenvalue_dict = {}
kpoint_index = 0

with open(ae_path) as ae:
	searchlines = ae.readlines()
	for i, line in enumerate(searchlines):
		if "(state, eigenvalue and occupancy below)" in line: 
			k = 1
			n = 0
			eigenvalue_dict = {}
			for l in searchlines[i+1:]: 
				if k != None:
					try:
						k = l[5]
					except IndexError:
						k = None 
					#should get first number on that line (the state) and it will continue					
					if k != None:
						n = n + 1
						#print l
						eigenvalue = float(l[6:20])
						eigenvalue_dict[n] = eigenvalue
					#gets eigenvalue for the line and adds it to a dictionary for that kpoint
				
			#print eigenvalue_dict		
			#a dictionary of a kpoint's eigenvalues

			kpoint_index = kpoint_index + 1
			kpoint_eigenvalue_dict[kpoint_index] = eigenvalue_dict
			#it's a dictionary of kpoint: eigenvalue_dictionary			

print "Dictionary for eigenvals was created."

#for kpoint_key in kpoint_eigenvalue_dict:
#	print kpoint_eigenvalue_dict[kpoint_key]

#print kpoint_eigenvalue_dict[1]
#print kpoint_eigenval_db_dict[1]


difference = 0
#print "should be small difference each time but add up."

for kpoint_key in kpoint_eigenval_db_dict:
	#for each of the kpoints
	ae_eigenvalues = kpoint_eigenvalue_dict[kpoint_key]
	db_eigenvalues = kpoint_eigenval_db_dict[kpoint_key]
	#eigenvalues dict for both db and ae dict

#	for eigenval_number in db_eigenvalues:
	for index in range(1, 4):
		eigenval_number = index

		#for eigenval in dict of eigenvals
		db_eigenvalue = db_eigenvalues[eigenval_number]
		ae_eigenvalue = ae_eigenvalues[eigenval_number]
		#eigenvalue for eigenvalue dict for db and ae

		#print ae_eigenvalue - db_eigenvalue
		difference += (ae_eigenvalue - db_eigenvalue)	
		#keeps sum of shift between each eigenvalue




print "\nAverage shift:"
avg_shift = difference/(4*number_kpoint)
print avg_shift
#add to table to know shift


cursor.execute('''INSERT INTO Kpoint_eigenvals(avg_shift) VALUES(?)''', (avg_shift,))



sum_eigenvals_shift = 0

for kpoint_key in kpoint_eigenval_db_dict:
        #for each of the kpoints
        ae_eigenvalues = kpoint_eigenvalue_dict[kpoint_key]
        db_eigenvalues = kpoint_eigenval_db_dict[kpoint_key]
        #eigenvalues dict for both db and ae dict

#        for eigenval_number in db_eigenvalues:
        for index in range(1, 4):
                eigenval_number = index

                #for eigenval in dict of eigenvals
                db_eigenvalue = db_eigenvalues[eigenval_number]
                ae_eigenvalue = ae_eigenvalues[eigenval_number]
                #eigenvalue for eigenvalue dict for db and ae

                sum_eigenvals_shift += (ae_eigenvalue - db_eigenvalue - avg_shift)**2

	
rms_eigenval = 27.2114*((sum_eigenvals_shift/(4*number_kpoint))**(.5))
#root mean square
print rms_eigenval






db.commit()
db.close()







