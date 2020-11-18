#!/bin/bash

# Install external dependendecies required to run GRAFIMO before integration 
# testing on http://travis-ci.org/:
# - vg
# - tabix
# - graphviz

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

