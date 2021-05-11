#!/bin/bash

# install miniconda (Linux 64bit)
apt-get upgrade -y
apt-get install curl -y
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -p "${HOME}/miniconda"
export PATH="${HOME}/miniconda/bin:${PATH}"

# add channels Linux
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

# install VG via bioconda
conda install vg -y

