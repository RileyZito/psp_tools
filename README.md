# psp_tools

psp_tools is a collection of programs that were written in the Summer of 2017 for the SHIP internship and NIST.

These programs were made to aid the OCEAN code by finding pseudo potential files for the user,
automatically running and storing data from the OPF stage of OCEAN, and allowing users to add new information and pseudo files.

finder codes- find the pseudo potential files for the user, copy files into working directory, and supply a citation file

adder codes- allow the user to add and overwrite znucl, semicore, and quality directories as well as copying pseudo files into new directories

updater, dir_creator, and codes that end with db- manipulate sqlite3 database and tables to replace directory system, 
or recreate it in a better way. This allows pseudo files, znucl, semicore, and quality information to be accessed easier
and be provided in a better way for the user. 

Terminology:

OCEAN code- a code created in part by my mentor John Vinson that is a theoretical tool used to examine the structure and electron movement
in crystal materials

znucl- atomic number of an element

semicore- which calculation to run depending on the structure of the electron levels in an element/material

quality- how many points/what depth the code needs to run to insure that an accurate model is created

pseudo potential files- files that supply important information about elements to OCEAN
