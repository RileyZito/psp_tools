# psp_tools

psp_tools is a collection of programs that were written by Mellie Zito in the Summer of 2017 for the SHIP internship at NIST.

These programs were made to aid the OCEAN code by finding pseudopotential files for the user,
automatically running and storing data from the OPF stage of OCEAN, and allowing users to add new information and pseudo files.

finder codes- find the pseudopotential files for the user, copy files into working directory, and supply a citation file

adder codes- allow the user to add and overwrite znucl, semicore, and quality directories as well as copying pseudo files into new directories

updater, dir_creator, and codes that end with db- manipulate sqlite3 database and tables to replace directory system, 
or recreate it in a better way. This allows pseudo files, znucl, semicore, and quality information to be accessed easier
and be provided in a more efficient way for the user. 

## Terminology:

- **OCEAN code**- a theoretical tool for calculating optical/UV and near-edge x-ray (XAS/RIXS) spectra in crystalline materials

- **znucl**- atomic number of an element

- **semicore**- whether or not the pseudopotential includes so-called semi-core electrons in the valence bands, e.g., 3s and 3p electrons in a 3d transition metal

- **quality**- directly related to the plane-wave energy cut-off (in Rydberg) needed for a given pseudopotential 

- **pseudopotential files**- files that supply important information about elements to OCEAN

## How to use database codes:

- **finder_db**- The user should fill out znucl, semicore, and pp.quality files in Common directory with the wanted values. When 
OCEAN or the user runs finder_db, the best entries fitting what was requested will be picked and then the pseudo files will be 
copied into the current directory for later use.

- **adder_db**- The code is interactive and will ask the user for specific files in order to fill out the new entry in the
database. For ease of use, it is suggested that the user copy all the necessary files (pseudo files and citation) to the 
current directory before using the code; however, it is not necessary. 

- **dir_creator**- The user simply give a location where a system of directories can be created (that doesn't 
already have the system of directories) and dir_creator will automatically copy all information from the database into files
under directories labeled by md5 fhi. Ex: user_location -> directories named by md5 fhi -> the specific files corresponding to each md5

- **updater**- If changes have been made to the directory system, the user can run updater to automatically check for updates
and updater will put this new information in the database. It should be noted that the information must be in the same
format. Ex: the file that contains the znucl must be named "znucl"
