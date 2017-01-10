# Reduction

## Introduction
The project idea is an algorithm to determine the number of XORs performed in the polynomial modular reduction. 

## Usage
It is possible to use the program. It is possible to use one single thread or multiples threads. 


## Dependences
To run the project it is needed to install  Xlsxwriter from http://xlsxwriter.readthedocs.org/en/latest/getting_started.html

### Single Thread
To use the single thread the usage is:
<pre><code>python single.py -i inputfile -o outputfile -d </code></pre>
inputfile - It is the input file with polynomials 
outputfile - It is the file with the results of the number of xors for each polynomial in the inputfile
d is for debug (optional)

### Multiple Threads
To use the multiple thread the usage is:
<pre><code>python main.py -i inputfile -o outputfile -t 4</code></pre>
inputfile - It is the input file with polynomials 
outputfile - It is the file with the results of the number of xors for each polynomial in the inputfile
t - It is the number of threads

### File with polynomials
The file with polynomials must be:
- One polynomial per line
- Polynomial in the format : x^m + x^a + x^b + ... + x + 1

#### Example of file 
```
x^19 + x^15 + x^3 + x + 1
x^19 + x^14 + x^13 + x^12 + 1
x^6 + x^5 + x^4 + x^3 + x^2 + x + 1
```
