#!/bin/bash
sudo python3 ghost_reg.py;
sudo mn -c; 
sudo rm -rf ./results/actuator/*.log ./results/receiver/*.log; 
sudo python custom_topo.py;
