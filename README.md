# psp_tools

psp_tools is a collection of programs that were written by Riley Zito in the summer of 2017 for the [Summer High School Intern Program (SHIP)](https://www.nist.gov/ohrm/summer-high-school-intern-program) at the [National Institute of Standards and Technology (NIST)](https://www.nist.gov/about-nist/our-organization/mission-vision-values).

These programs were made to aid the [OCEAN code](www.ocean-code.com) by finding pseudopotential files for the user, storing data from the OPF stage of OCEAN, and allowing users to add new information and pseudopotential files to a database or system of directories.

- **finder codes**- find the pseudopotential files for the user, copy files into working directory, and supply a citation file

- **adder codes**- allow the user to add and overwrite stored znucl, semicore, and quality information as well as adding corresponding pseudopotential files to the storage system.

- **updater, dir_creator, and codes that end with db**- manipulate sqlite3 database and tables to replace the directory system, 
or recreate it in a better way. This allows pseudo files, znucl, semicore, and quality information to be accessed easier
and be provided in a more efficient way for the user. 

## Terminology:

- **OCEAN code**- a theoretical tool for calculating optical/UV and near-edge x-ray (XAS/RIXS) spectra in crystalline materials.

- **znucl**- atomic number of an element.

- **semicore**- whether or not the pseudopotential includes so-called semi-core electrons in the valence bands, e.g., 3s and 3p electrons in a 3d transition metal.

- **quality**- higher numbers generally run more accurate calculations but cost more time. The numbers are directly related to the plane-wave energy cut-off (in Rydberg) needed for a given pseudopotential. 

- **pseudopotential (psp) files**- files that supply important information about elements to OCEAN.

## How to use database codes:

- **finder_db**- The user should fill out znucl, semicore, and pp.quality files in Common directory with the wanted values. When OCEAN or the user runs finder_db, the best entries fitting what was requested will be picked and then the pseudo files will be copied into the current directory for later use.

- **adder_db**- The code is interactive and will ask the user for specific files in order to fill out the new entry in the
database. For ease of use, it is suggested that the user copy all the necessary files (pseudo files and citation) to the 
current directory before using the code; however, it is not necessary. 

- **dir_creator**- The user simply gives a location where a system of directories can be created (that doesn't already have the system of directories) and dir_creator will automatically copy all information from the database into files under directories labeled by md5 fhi. user_location -> directories named by md5 fhi -> the specific files corresponding to each md5

- **updater**- If changes have been made to the directory system, the user can run updater to automatically check for updates
and updater will put this new information in the database. It should be noted that the information must be in the same
format. Ex: the file that contains the znucl must be named "znucl"

- **opf_adder_db**- The code is interactive and will ask the user for specific files to double check the database
and then know which entry in the main table and pseudos table correlates with the OPF information that will be added.
After the file names are entered and checked, the user will have to decide whether to update or overwrite a pre-existing
entry. If there is no current entry for the information provided, then a new one will be created automatically. At the
end of this code, the tables core_potential and radii_info should have all the information the OPF stage would generate if ran. 

- **psp_adder_db**- This code is only interactive in the beginning when it will ask the user for input files. For each input file, the file will be copied into the correct directory, corrected and then oncvpsp.x will be ran on this file to create the out file. The parser.py script will be ran with this out file to extract the important needed information. That information (znucl, semicore, quality, psuedopotential files, and citation) will be inputted into adder_db.py. This allows for the database to be updated with multiple psuedopotential files even when they are in a different format.
