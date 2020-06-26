#!/bin/bash
sudo python3 ghost_reg.py $1;
sudo mn -c; 
sudo rm -rf ./results/actuator/*.log ./results/receiver/*.log; 
sudo python custom_topo.py $1 $2 $3;
