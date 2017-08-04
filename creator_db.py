import sqlite3, os, sys

try:
	open('psps.db')
	print "Database already exists. If you would like to create a new database, delete the old one."
	sys.exit(1)
	#if open works, the database already exists and this code stops

except IOError as e:
	if e.args[0] == 2:
		db = sqlite3.connect('psps.db')
		print "psps.db was created."
	#IOError.args[0] == 2 is the "no such file or directory" error. If that pops up, create the new database
	else:
		print e
		sys.exit(1)
	#if it's any other error just stop the code


cursor = db.cursor()

cursor.execute(''' CREATE TABLE main( id INTEGER PRIMARY KEY, z INTEGER, qf INTEGER, semicore TEXT ) ''' )
cursor.execute(''' INSERT INTO main(id, semicore ) VALUES(?, ?)''', (None, "don't delete this entry.",))
#If you don't specify the primary key then sqlite automatically picks one higher than the highest, so should be 0 or 1 here

cursor.execute(''' CREATE TABLE pseudos( id INTEGER, md5_fhi TEXT PRIMARY KEY, fhi_name TEXT, fhi TEXT, md5_upf TEXT, upf_name TEXT, upf TEXT, citation TEXT, opts_name TEXT, opts TEXT, fill_name TEXT, fill TEXT) ''' )

cursor.execute(''' CREATE TABLE core_potential( id INTEGER PRIMARY KEY, md5_fhi TEXT, N INTEGER, L INTEGER, vc_bare TEXT, vpseud1 TEXT, vvallel TEXT) ''') 
cursor.execute(''' INSERT INTO core_potential( id, vc_bare) VALUES(?, ?)''', (None, "don't delete this entry.",))

cursor.execute(''' CREATE TABLE radii_info( id INTEGER, radius REAL, text_file TEXT ) ''')
#creates all the different tables needed

print "psps.db tables have been created."
