iodb
====
This project provides scripts creating a US input-output database directly from 
the [BEA statistics](http://www.bea.gov/industry/io_benchmark.htm). It creates
a direct requirement matrix from the BEA make and use tables. This DR matrix is 
than combined with a satellite matrix and converted to a set of process dates 
sets in the [olca-schema](https://github.com/GreenDelta/olca-schema) which can
be imported into [openLCA](http://www.openlca.org/). The satellite matrix is 
based on the satellite matrix of the OpenIO database but was mapped to the flows 
of the openLCA reference list.


The CSV matrix format of the make and use tables
------------------------------------------------
The raw make and use tables are first converted into a CSV file format which
describes a matrix with 3 columns: row-label, column-label, value. The labels
are strings that uniquely identify a sector. In the use table commodities are
listed in the rows (1. column of the CSV file) and industries are listed in the
columns (2. column of the CSV file). In the make table it is the other way 
around: industries are listed in the rows (1. column of the CSV file) and 
commodities in the columns (2. column of the CSV file).

The `iodb.csvmatrix` module helps to read and write such CSV matrix files:

    import iodb.csvmatrix as csvm
    
    matrix = csvm.read_sparse(path_to_csv_file)
    ...


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

Module dependencies
-------------------
http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy



License
-------
Unless stated otherwise, all source code of the this project is licensed under 
the [Mozilla Public License, v. 2.0](https://www.mozilla.org/MPL/2.0/).

