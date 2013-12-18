#!/bin/bash

set -e

python setup.py develop

source ./installrc

echo "Installing Configs"
sudo ./install_configs.sh

echo "Building and Install Pylucene this could take a few minutes...."
./install_pylucene.sh
