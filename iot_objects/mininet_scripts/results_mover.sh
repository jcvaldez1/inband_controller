#!/bin/bash
#sudo rm -rf experiments/results;
sudo cp -R results/ experiments/$2;
sudo python3 module_parser.py $1 $2
sudo rm -rf ./results/actuator/*.log ./results/receiver/*.log; 
