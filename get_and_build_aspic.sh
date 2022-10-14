#!/bin/bash
wget http://cp3.irmp.ucl.ac.be/~ringeval/upload/patches/aspic/aspic-0.3.2.tar.gz
tar xf aspic-0.3.2.tar.gz
cd aspic-0.3.2
mkdir build
./configure --prefix=${PWD}/build
make
make install
cd ..
cp aspic-0.3.2/build/lib/libaspic.a .
python generate_wrapper.py
python setup.py build_ext -i
python -c 'import pyaspic'
