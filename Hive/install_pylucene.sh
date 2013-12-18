#!/bin/bash

set -e

hash ant 2> /dev/null || { echo >&2 "I require ant but it's not installed.  Aborting."; exit 1; }
hash make 2> /dev/null || { echo >&2 "I require make but it's not installed.  Aborting."; exit 1; }
hash gcc 2> /dev/null || { echo >&2 "I require gcc but it's not installed.  Aborting."; exit 1; }

if [ ! -f pulucene-4.5.1-1-src.tar.gz ]; then
  wget "http://mirror.ox.ac.uk/sites/rsync.apache.org/lucene/pylucene/pylucene-4.5.1-1-src.tar.gz"
fi

tar xzf "pylucene-4.5.1-1-src.tar.gz"
pushd "pylucene-4.5.1-1"

pushd jcc

echo "Variables set:"
echo "$JCC_JDK"

echo "Building JCC"
python setup.py build

echo "Building Installing JCC"
python setup.py install

popd 

echo "Making Pylucene..."
make

set +e

echo "Testing build..."
make test 

echo "Installing..."
sudo -E make install 

popd 

echo "Cleaning up..."
rm -r "pylucene-4.5.1-1"
