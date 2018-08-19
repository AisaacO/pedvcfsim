# pedvcfsim
Simulate vcf file from pedigree data using a finite table Chinese restaurant process.

<p align="center"><img width=40% src="https://github.com/AisaacO/pedvcfsim/blob/master/images/vcfsim.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v2.7%20%2F%20v3.6-blue.svg)
[![Build Status](https://travis-ci.org/anfederico/Clairvoyant.svg?branch=master)](https://travis-ci.org/anfederico/Clairvoyant)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/Clairvoyant.svg)](https://github.com/anfederico/Clairvoyant/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
----
The simulation follows a descrete time stochastic finite mixture model similar to seating customers in a Chinese restaurant. The application restricts tables in the process to 4 corresponding to the bases ```'A', 'G', 'C', 'T'.``` 


---------------------------------------
# Getting Started
---------------------------------------

This README should get you started with your Simulation

License information can be found in the accompanying LICENSE file. 

pedvcfsim requires python version 3+, it is simple to use and only requires python base modules.

##### Download
T

----

##### Pedigree File Format

```pedtovcfsim``` requires a 5-column, tab-separated pedigree file format as input
```
I_ID	F	M	S	S_ID
1   0   0   1   Sample1
2   0   0   2   Sample2
3   1   2   2   Sample3
```
F_ID = Family ID

I_ID = Individual ID

F = Father ID

M = Mother ID

S = Sex

S_ID = Sample ID

----

##### Example Usage:

python pedtovcfsim.py -i test.ped -t 0.25 -n 1 -e 0.005 -c 30 -m 3 -a 2 -s 99 -o test.vcf

To get help on usage parameters, just type ```python pedvcfsim.py -h```


