iodb
====
This project provides modules and scripts for creating an environmental input
output database based on the OpenIO framework. The data that are produced by
this project can be directly used in LCA software tools like openLCA and 
SimaPro. The project contains a command line tool `iodb` with which the 
respective artifacts can be created from the raw data in the `data` folder. 

Running the tool
----------------
You need to have Python 3.x installed in order to run the `iodb` tool. To use 
the tool open a command line in the project directory and type `iodb` followed 
by the respective task you want to execute, e.g. 

    iodb clean
    
will delete the content of the `build` directory. You can also execute multiple
commands, e.g.

    iodb clean all
    
will first delete all resources from the build directory, re-build all 
resources, and create a zip file containing all data sets in the EcoSpold 1 
format.  

Implemented tasks
-----------------

    iodb help
    
Prints the help to the command line.

    iodb clean
    
Deletes all files from the build directory.

    iodb tech
    
Creates the direct requirements matrix from the BEA input output statistics.

    iodb products
    
Creates the table with product information for the commodities in the direct
requirement matrix.

    iodb sat
    
Creates the satellite matrix containing the elementary flow, material, and waste
entries for the commodities in the direct requirement matrix.

    iodb flows
    
Creates a table with meta-information for the flows in the satellite matrix.
 
    iodb spold
    
Creates a zip file with process data sets in the EcoSpold format from the 
resources created from the tasks above. The resulting zip file can be directly
imported into openLCA.

    iodb all
    
Currently the same as `spold`: executes all tasks to create the database in
EcoSpold format.

The tasks produce files in a standard text format (mostly CSV) that can be 
easily processed by other tasks. If a task requires the resources from another
task it firts calls this task. If a resource is already present in the build
folder it will not created again.

As the tasks use simple text based data formats it is easy to write additional
tasks (e.g. flow mappings) or add other data sources.

Data sources
------------
* [BEA 2002 benchmark files](http://www.bea.gov/industry/io_benchmark.htm)
* ...

License
-------
Unless stated otherwise, all source code of the this project is licensed under 
the [Mozilla Public License, v. 2.0](https://www.mozilla.org/MPL/2.0/).

