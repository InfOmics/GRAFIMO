# GRAFIMO
Graph-based Find Individual Motif Occurrences

## GRAFIMO installation and usage
**dependencies needed**

**pip installation**

**docker image**

## installation test
 If everything went right type:
 ```
 grafimo --help
 ```
 if the help is correctly printed, then the tool is installed.

 To test the functionalities of GRAFIMO download the directory test.
 Enter it, by typing:
 ```
 cd tests
 ```

 Then type:
 ```
 grafimo_test
 ```
If at the end appears the message:
"All tests passed! Enjoy GRAFIMO for your research!"
All the tests were passed.

Remember to exit from the test directory with:
```
cd ..
```

## Usage

Here is a brief guide to help you using GRAFIMO.

We provide the user with two possible workflows:
- with the variation graph creation
- using the user variation graph

**with variation graph creation**
Input:
- linear reference genome in .fa format (e.g. hg38.fa)
- VCF file compressed (e.g. my_vcf.vcf.gz)
- BED file containing the regions to extract from the genome
- JASPAR motif file (available at http://jaspar.genereg.net/)
- [OPTIONS]

Output:
- CSV file containing the sequences statistically significant with their scores

Example:
```
grafimo --


**
