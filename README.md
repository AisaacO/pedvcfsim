<p align="center"><img width=12.5% src="https://github.com/AisaacO/pedvcfsim/blob/master/images/logo.png"></p>
<p align="center"><img width=40% height=5% src="https://github.com/AisaacO/pedvcfsim/blob/master/images/words.png"></p>
Simulate Variant Call Format (VCF) file from pedigree or graph like data using a finite table Chinese restaurant process.
The simulation follows a descrete time stochastic finite mixture model similar to seating customers in a Chinese restaurant. Tables in the process are restricted to 4, corresponding to the bases 'A', 'G', 'C', 'T'. 


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
##PEDNG v1.0
##I_ID	F	M	S	S_ID
1   .   .   1   Sample1
2   .   .   2   Sample2
3   1   2   2   Sample3
```

First Column  = Individual ID

Second Column = Father ID

Third column = Mother ID

Fourth column = Sex

Fifth column = Sample ID

----

### Coverage Format

```Assign values based on how much coverage you want for founders or parents in your pedigree vs offsprings. If there are more than one (1) samples in your file, the coverage is equally shared among your samples ```

For example:

Number of parents = 2, Coverage = 20X, Each parent gets 10X
Number of children = 2, Coverage = 40X, Each child gets 20X

Number of parents = 2, Number of samples = 2, Coverage = 20X, Each parent gets 5X, Each samples gets 5X

Number of children = 2, Number of samples = 2, Coverage = 40X, Each child gets 10X, Each sample gets 10X


### Zygosity Format

```Assign values based on zygosity type if twins occur in the pedigree. Three (3) values are assigned to z ```

If the twins are Monozygotes, z starts with 1 but if Dizygotes, z starts with 2.

Next, provide values for the twins:

Values can be strings (names of the twins), integers (values for the twins) or combined string and integer twin names

```Monozygotes: -z 1 A B or -z 1 3 4 or -z 1 A 4```

```Dizygotes:   -z 2 A B or -z 2 2 4 or -z 2 B 4```


##### Example Usage:

python pedtovcfsim.py -i test.ped -t 0.25 -n 1 -e 0.005 -c 20 60 -m 3 -a 2 -s 99 -o test.vcf   [No twin in pedigree]

python pedtovcfsim.py -i test.ped -t 0.25 -n 1 -e 0.005 -c 20 60 -m 3 -a 2 -z 1 3 4 -s 99 -o test.vcf [twin in pedigree]

To get help on usage parameters, just type ```python pedvcfsim.py -h```

### Code of Conduct

To contribute, please read [CONTRIBUTING.md](https://github.com/AisaacO/pedvcfsim/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us. 

### Issues & bug reports
If you have feature requests or bug reports, feel free to help out by sending pull requests or by [creating new issues](https://github.com/AisaacO/pedvcfsim/issues/new). Please take a moment to
review the guidelines [Here](https://github.com/AisaacO/pedvcfsim/GUIDELINES.md):

* [Bug reports](https://github.com/AisaacO/pedvcfsim/blob/master/GUIDELINES.md#bugs)
* [Feature requests](https://github.com/AisaacO/pedvcfsim/blob/master/GUIDELINES.md#features)
* [Pull requests](https://github.com/AisaacO/pedvcfsim/blob/master/GUIDELINES.md#pull-requests)

## Authors

* **Isaac Akogwu** - *Phase I-III* - [Pedvcfsim](https://github.com/AisaacO/pedvcfsim)


