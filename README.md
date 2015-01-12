iodb
====
This project provides modules and scripts for creating an environmental input
output database based on the OpenIO framework. The data that are produced by
this project can be directly used in LCA software tools like openLCA and 
SimaPro. 

The project contains a command line tool `iodb` with which the respective
artifacts can be created from the raw data in the `data` folder. You need to
have Python 3.x installed in order to run this tool. To use the tool open a 
command line and type `iodb` followed by the respective task you want to 
execute, e.g. 

    iodb clean
    
will delete the content of the `build` directory. You can also execute multiple
commands, e.g.

    iodb clean all package
    
will first delete all build resources, re-build all resources, and create a zip
file containing all data sets in the EcoSpold 1 format. 

clean
-----





Data sources
------------
* [BEA 2002 benchmark files](http://www.bea.gov/industry/io_benchmark.htm)
* ...

License
-------
Unless stated otherwise, all source code of the this project is licensed under 
the [Mozilla Public License, v. 2.0](https://www.mozilla.org/MPL/2.0/).

