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
grafimo --linear_genome hg.fa --vcf vcf.vcf.gz --bedfile bed.bed --motif m.jaspar [OPTIONS]
```

**without variation graph creation**

Input:
- your variation graph both in VG and XG format (better if in XG)
- BED file containg the regions to extract from the genome
- JASPAR motif file (available at http://jaspar.genereg.net/)
- [OPTIONS]

Output:
- CSV file containing the sequences statistically significant with their scores

Example:
```
grafimo --graph_genome my_vg.xg --bedfile my_bed.bed --motif my_motif.jaspar
```

**Advanced examples**

If you want to try advanced examples to take a look into GRAFIMO functionlities
download the ```test``` directory and enter it, by typing:
```
cd test/fullpipeline
```

Let's start with an example showing the creation of the variation graph.
Run the script ```getdata_fullpipeline.sh```, by typing on your terminal:
```
getdata_fullpipeline
```

We will get a file ```hg38.fa```, that is the fasta file for the genome assembly
GRCh38 and a vcf file ```ALL.wgs.shapeit2_integrated_snvindels_v2a.GRCh38.27022019.sites.vcf.gz.vcf.gz```
from the 1000 Genome Project.

With them we will create our variation graph. Be patient this step will take
some time.

In the current directory we have a BED file ```200peaks.bed```, in this file
there are the first 200 best peaks for CTCF from ChIP-seq data by The ENCODE
Project (ENCFF519CXF.bed)

You will also find the motif file ```MA0139.1.jaspar``` representing the CTCF
motif from JASPAR database (http://jaspar.genereg.net/) and ```bg_nt```. The
latter file represents a background distribution for the alphabet.

Now we are ready to try the tool. Type:
```
grafimo --linear_genome hg38.fa --vcf ALL.wgs.shapeit2_integrated_snvindels_v2a.GRCh38.27022019.sites.vcf.gz.vcf.gz --bedfile 200peaks.bed --motif MA0139.1.jaspar --bgfile bg_nt
```

You can also set the p-value threshold to use by adding to the command line ```--pvalueT 1e-3```.

It is possible to set the pseudocount to add to the motif counts, by adding the
argument ```--pseudo 0.1``` to the command line

If you like you can also define an output directory name, where results will be
placed, by adding the option ```--o my_result_dir``` to the command line.

If you prefer to score only sequences belonging to the forward strand you can
add the option ```--no_reverse```to the command line.

When all is finished you should find a directory named ```grafimo_out``` (or
the name that you give it using the ```--o``` option).
Enter it and you will find a CSV file ```grafimo_out.csv``` with the scoring results.



If you have your own variation graph available in VG or XG format you can skip
the variation graph creation step.

To test this pipeline download and go to the ```test``` directory with:
```
cd test/myvgpipeline
```

Here there is a toy example of the variation graph of the chromosome 22,
named ```chr22.xg```. Remember that also the VG format is allowed, but its
processing will take more time since we need to index it.

In the current directory we have a BED file ```200peaks.bed```, in this file
there are the first 200 best peaks for CTCF from ChIP-seq data by The ENCODE
Project (ENCFF519CXF.bed)

You will also find the motif file ```MA0139.1.jaspar``` representing the CTCF
motif from JASPAR database (http://jaspar.genereg.net/) and ```bg_nt```. The
latter file represents a background distribution for the alphabet.

Now we are ready to try the tool. Type:
```
grafimo --graph_genome chr22.xg --bedfile 200peaks.bed --motif MA0139.1.jaspar --bgfile bg_nt
```

You can also set the p-value threshold to use by adding to the command line ```--pvalueT 1e-3```.

It is possible to set the pseudocount to add to the motif counts, by adding the
argument ```--pseudo 0.1``` to the command line

If you like you can also define an output directory name, where results will be
placed, by adding the option ```--o my_result_dir``` to the command line.

If you prefer to score only sequences belonging to the forward strand you can
add the option ```--no_reverse```to the command line.

When all is finished you should find a directory named ```grafimo_out``` (or
the name that you give it using the ```--o``` option).
Enter it and you will find a CSV file ```grafimo_out.csv``` with the scoring results.



