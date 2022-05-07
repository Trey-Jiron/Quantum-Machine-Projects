
This is the code for the VQE for a hydrogen molecule I worked on as a senior project in 2020, based 
Mostly on data from O'Malley et al(2016). The code uses IBM's quantum machine so will require an 
IBM account on disk to run. The results can then be plotted into a heat map or 3d map. The breakdown of 
The files follows:

VQE.py main code that sends the circuits to the quantum machine to run and records all the data and 
Produces .txt files with the data.

Heatmap.py code to calculate the hamiltonian value for all r and theta and can graph it either as a heat map
Or a 3d graph. Also plots individual expectation values against theoretical data along with a single example
Hamiltonian for r= 0.75

Research progress report, report written at the end of work, should summarize theory behind it and the
Results

pea_table_formated.tex: table that lists all the constants for the calculations for the different r, read by the 
Code to calculate H, needed in the same directory as code for heat map  code to work

Example results: results that should be given after running this code, all the text files and figures. Text files
Are also in the main file since the it is needed for the heat map code.

If there are any questions or bugs you can post it on GitHub or email me at treyjiron@gmail.com}
