#!/bin/bash

echo "Installing Dependencies..."
sudo apt-get update
sudo apt-get install -y python-software-properties python g++ make gcc make ant openjdk-7-jdk python-dev curl nodejs screen rabbitmq-server mongodb-server
sudo curl http://npmjs.org/install.sh -L -o -| sudo sh

echo "Installing Hive..."
pushd Hive
cp installrc.example installrc
python ez_setup.py
./install.sh
cp localrc.example localrc
popd 
echo "Done..."

echo "Installing Queen..."
pushd Queen
cp config/config.js.example config/config.js
npm install
popd
echo "Done..."

echo "Installing Bee..."
pushd Agents/BEE\ Client
cp etc/config.js.example config.js
npm install 
popd
echo "Done..."

