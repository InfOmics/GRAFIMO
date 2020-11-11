#!/bin/bash

# Install external dependendecies required to run GRAFIMO before integration 
# testing on http://travis-ci.org/:
# - vg
# - tabix
# - graphviz

# solve dependencies required by vg
sudo apt-get install bc 
sudo apt-get install rs 
sudo apt-get install jq
sudo apt-get install samtools
sudo apt-get install cmake
sudo apt-get install protobuf-compiler
sudo apt-get install libprotoc-dev
sudo apt-get install libprotobuf-dev
sudo apt-get install libjansson-dev
sudo apt-get install libbz2-dev
sudo apt-get install libncurses5-dev
sudo apt-get install automake
sudo apt-get install libtool
sudo apt-get install curl
sudo apt-get install unzip
sudo apt-get install redland-utils
sudo apt-get install librdf-dev
sudo apt-get install pkg-config
sudo apt-get install wget 
sudo apt-get install gtk-doc-tools
sudo apt-get install raptor2-utils
sudo apt-get install rasqal-utils
sudo apt-get install bison
sudo apt-get install flex
sudo apt-get install gawk
sudo apt-get install libgoogle-perftools-dev
sudo apt-get install liblz4-dev
sudo apt-get install liblzma-dev
sudo apt-get install libcairo2-dev
sudo apt-get install libpixman-1-dev
sudo apt-get install libffi-dev
sudo apt-get install doxygen
                     
# precompiled binaries are no more available for vg, so build it from source
git clone --recursive https://github.com/vgteam/vg.git
cd vg
# we should already have solved VG's dependencies
make get-deps
# start build
chmod +x ./source_me.sh
. ./source_me.sh && make

# tabix already comes with vg

# exit from vg directory and make sure it is available in the path
cd ..
vg find

