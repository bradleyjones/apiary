#!/bin/bash

echo "Installing Dependencies..."
sudo apt-get update
sudo apt-get install -y python-software-properties python g++ make gcc make ant openjdk-7-jdk python-dev curl nodejs
sudo curl http://npmjs.org/install.sh -L -o -| sudo sh

echo "Installing Hive..."
pushd Hive
python ez_setup.py
./install.sh
popd 
echo "Done..."

echo "Installing Queen..."
pushd Queen
npm install
popd
echo "Done..."

echo "Installing Bee..."
pushd Agents/BEE\ Client
npm install 
popd
echo "Done..."

