<p align="center"><img width=12.5% src="https://github.com/AisaacO/pedvcfsim/blob/master/images/logo.png"></p>
<p align="center"><img width=40% height=5% src="https://github.com/AisaacO/pedvcfsim/blob/master/images/words.png"></p>
Simulate Variant Call Format (VCF) file from pedigree or graph like data using a finite table Chinese restaurant process.
The simulation follows a descrete time stochastic finite mixture model similar to seating customers in a Chinese restaurant. Tables in the process are restricted to 4, corresponding to the bases ```'A', 'G', 'C', 'T'.``` 


----


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Python-v3.6%2B-blue.svg)
[![Build Status](https://travis-ci.org/AisaacO/pedvcfsim.svg?branch=master)](https://travis-ci.org/AisaacO/pedvcfsim)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub issues](https://img.shields.io/badge/Issues-2%20open-orange.svg)](https://github.com/AisaacO/pedvcfsim/issues)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](https://github.com/AisaacO/pedvcfsim/blob/master/CONTRIBUTING.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


---------------------------------------
# Getting Started


This README should help get you started with your Simulation

License information can be found in the accompanying LICENSE file. 

pedvcfsim requires python version 3+, it is simple to use and only requires python base modules.

### Installation
To use pedvcfsim, you can either clone or download by:

* running `git clone git@github.com:AisaacO/pedvcfsim.git` on your local Linux machine to clone the repo 
* Click [Download](https://github.com/AisaacO/pedvcfsim/archive/master.zip) to download the zip folder

----

### Pedigree File Format

```pedtovcfsim``` requires a 5-column, tab-separated pedigree file format as input
```
I_ID	F	M	S	S_ID
1   0   0   1   Sample1
2   0   0   2   Sample2
3   1   2   2   Sample3
```

First Column  = Individual ID

Second Column = Father ID

Third column = Mother ID

Fourth column = Sex

Fifth column = Sample ID

----

##### Example Usage:

python pedtovcfsim.py -i test.ped -t 0.25 -n 1 -e 0.005 -c 30 -m 3 -a 2 -s 99 -o test.vcf

To get help on usage parameters, just type ```python pedvcfsim.py -h```

### Contribution

To contribute, please read [CONTRIBUTING.md](https://github.com/AisaacO/pedvcfsim/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us. 

## Authors

* **Isaac Akogwu** - *Phase I-III* - [Pedvcfsim](https://github.com/AisaacO/pedvcfsim)


