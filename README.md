OpenIO+
=======

Currently we convert the data from the OpenIO download package (this package is not online anymore?) to a set of CSV files:

* oio\_commodities.csv contains the commodity codes and names. This file is converted from the direct requirement matrix of the OpenIO technology module (DR Coefficients.xlsx, see oio\_dr\_to\_csv.py).  

* oio\_dr\_entries.csv contains the non-zero entries of the direct requirement matrix of the OpenIO technology module (DR Coefficients.xlsx, see oio\_dr\_to\_csv.py). The file has the following columns:

	1. the code of the input commodity
	2. the code of the receiving commodity
	3. the value in $/$  

* oio\_make.csv contains the entries of the raw make table of the OpenIO technology module (Raw Make Matrix.xlsx, see oio\_make\_to\_csv.py).

* 
 

BEA 2002 benchmark files:
http://www.bea.gov/industry/io_benchmark.htm