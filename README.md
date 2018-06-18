# pedvcfsim
Simulation of Meiosis and vcf file from pedigree data using a finite table Chinese restaurant process.

----

The script requires a pedigree file with 6 columns to simulate a variant call file with mutations at a user specified site. The simulation follows a descrete time stochastic finite mixture model similar to seating customers in a Chinese restaurant. The application restricts tables in the process to 4 corresponding to the bases ```'A', 'G', 'C', 'T'.``` 

pedtovcfsim requires python version 3+, it is simple to use and only requires python base modules.

----

##### Pedigree File Format

```pedtovcfsim``` requires a 6-column, tab-separated pedigree file format as input
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

##### Usage:

python pedtovcfsim.py -i test.ped -t 0.25 -n 1 -e 0.005 -c 30 -m 3 -a 2 -s 99 -o test.vcf

To get help on usage parameters, just type ```python pedvcfsim.py -h```


