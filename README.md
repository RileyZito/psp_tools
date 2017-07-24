# psp_tools

psp_tools is a collection of programs that were written in the Summer of 2017 for the SHIP internship and NIST.

These programs were made to aid the OCEAN code by finding pseudo potential files for the user,
automatically running and storing data from the OPF stage of OCEAN, and allowing users to add new information and pseudo files.

finder codes- find the pseudo potential files for the user, copy files into working directory, and supply a citation file

finder_db- a special version of finder that uses a sqlite database and does the additional step of running and storing data from OPF stage

adder codes- allow the user to add and overwrite znucl, semicore, and quality directories as well as copying pseudo files into new directories

Terminology:

OCEAN code- a code created in part by my mentor John Vinson that is a theoretical tool used to examine the structure and electron movement
in crystal materials

znucl- atomic number of an element

semicore- which calculation to run depending on the structure of the electron levels in an element/material

quality- how many points/what depth the code needs to run to insure that an accurate model is created

pseudo potential files- files that supply important information about elements to OCEAN
