#!/bin/bash

set -e

wget "http://mirror.ox.ac.uk/sites/rsync.apache.org/lucene/pylucene/pylucene-4.5.1-1-src.tar.gz"
tar xzf "pylucene-4.5.1-1-src.tar.gz"
cd "pylucene-4.5.1-1"

pushd jcc

python setup.py build
sudo python setup.py install

popd 

vim Makefile

make

sudo make test 

sudo make install 
