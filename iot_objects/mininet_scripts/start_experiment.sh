#!/bin/bash
sudo mn -c; 
sudo rm -rf ./results/actuator/*.log ./results/receiver/*.log; 
sudo python custom_topo.py
