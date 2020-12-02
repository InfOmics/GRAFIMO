#!/bin/bash

#----------------------------------------------------------
#
# This shell script shows how to build a genome variation
# graph with GRAFIMO, from a reference genome and a VCF file
#
# This example creates a VG using as reference the FASTA
# file data/xy.fa and xy2.vcf.gz. These files are simple 
# toy examples.
#
# In xy.fasta are contained the sequences for two toy
# chromosomes, named 'x' and 'y'. 
#
# The VCF file xy2.vcf.gz contains variants (SNPs and 
# indels) falling on both 'x' and 'y'. For each sequence
# are available two haplotypes.
#
#----------------------------------------------------------

# assign the reference genome FASTA and the VCF file to
# variables
reference="data/xy.fa"
vcf="data/xy2.vcf.gz"



# GRAFIMO will create a genome variation graph for each
# chromosome available in the reference FASTA file, in
# our example 'x' and 'y'
#
# The two resulting VGs will be indexed obtaining the XG
# index and the GBWT index
#
# The latter index allows to retrieve the haplotypes when
# scanning the VG

# Now we can call GRAFIMO to build our genome VG 
grafimo buildvg -l $reference -v $vcf

# As you can see, in the current directory appeared four
# new files 'chrx.xg', 'chrx.gbwt', 'chry.xg' and 'chry.gbwt'
#
# These are the VGs for chromosome 'x' and 'y', enriched with 
# the genomic variants contained in the given VCF file
#
# We can use `vg view` command to inspect the structure 
# of the VGs
vg view -dp chrx.xg - | dot -Tpng -o chrx.png 
vg view -dp chry.xg - | dot -Tpng -o chry.png 



# Now, let us assume we are interested in creating the VG
# only for chromosome 'x' from our reference FASTA
#
# Moreover, let us assume we want to store the resulting 
# VG in 'chrx_vg' directory
#
# This can be easily using `-c`  and `-o` options 
# when calling GRAFIMO from command-line
mkdir -p chrx_vg  # create the output directory

grafimo buildvg -l $reference -v $vcf -c x -o chrx_vg

# You can notice that in chrx_vg directory has been 
# built the VG only for chromosome 'x'



# Now let us assume we would like to build again the 
# genome VG (a variation graph for each chromosome)
# but using a fresher VCF index (TBI) file.
#
# This can be done adding `--reindex` option to 
# GRAFIMO's command-line call. Let us store the result
# in a new directory called 'vg_fresh_index'
mkdir -p vg_fresh_index  # create the output directory

grafimo buildvg -l $reference -v $vcf -o vg_fresh_index --reindex

# As you can see, in 'vg_fresh_index' are contained the VGs
# for both chromosomes 'x' and 'y' (XG and GBWT indexes) built
# using a fresher VCF index. 
#
# Their structure is identical to the original VGs



# For more options and a deeper look see https://github.com/InfOmics/GRAFIMO/wiki





