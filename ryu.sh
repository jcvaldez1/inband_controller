#!/bin/bash
# Install RYU (Ubuntu 14.04.3)
# Author: Oleg Slavkin

echo "Step 1. Install tools"
sudo apt-get -y install git python-pip python-dev

echo "Step 2. Install python packages"
sudo apt-get -y install python-eventlet python-routes python-webob
python-paramiko

echo "Step 3. Clone RYU git Repo"
git clone --depth=1 https://github.com/osrg/ryu.git

echo "Step 4. Install RYU"
sudo pip install setuptools --upgrade
sudo python ./ryu/setup.py install

echo "Step 5. Install and Update python packages"
sudo pip install six --upgrade
sudo pip install oslo.config msgpack-python
sudo pip install eventlet --upgrade

echo "Step 6. Extra Requirements"
sudo pip install -r ~/ryu/tools/pip-requires
sudo python ~/ryu/setup.py install

echo "Step 7. Test ryu-manager"
ryu-manager --version
