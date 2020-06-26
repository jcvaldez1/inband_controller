#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info
import subprocess
import datetime
import sys

def myNetwork(containers, host_count, split):
    hosts = [];
    container_number = int(containers)
    host_num = int(host_count)
    container_split = 100/int(split)
    max_id = host_num/container_split
    net = Mininet( topo=None,
                   build=False, controller = OVSController)

    info( '*** Adding controller\n' )
    net.addController(name='c0')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    Intf( 'eno2', node=s1 )

    for x in range(0, host_num):
        host_name = 'h'+str(x)
        h = net.addHost(host_name, ip='0.0.0.0')
        hosts.append(h)
        net.addLink(h, s1)


    info( '*** Starting network\n')
    net.start()
    for h in hosts:
        h.cmdPrint('dhclient '+h.defaultIntf().name)

    # register
    CLI(net)
    confirm = str(raw_input("run test? y or n "))
    container_counter = 0
    while confirm != "n":
        for x in range(0, host_num):
            if x/max_id > container_counter:
                container_counter += 1
            if x % 2 == 0:
                cmdstring = "python3 actuator.py 1000 0.5 "+ str(x%max_id)+ " 52.74.73."+str((container_counter*2)+2)
            else:
                cmdstring = "python receiver.py "+str((x%max_id))+ " 13.55.147."+str((container_counter*2)+1)
            hosts[x].cmdPrint(cmdstring+" &")
        raw_input("parse results? ")
        ps_string = subprocess.check_output(["ps","-ef"]).split("\n")
        pid_string = [x for x in ps_string if ("python" in x)]
        print(pid_string)
        for x in pid_string:
           if not ("custom_topo" in x):
              stringy = filter(None, x.split(" "))[1]
              hosts[0].cmdPrint("kill "+str(stringy))

        curr_time = str(datetime.datetime.now().strftime("%H:%M:%S"))
        cmd_list = "./results_mover.sh "+str(max_id)+" "+ curr_time+" "+str(container_number)
        subprocess.call(cmd_list, shell=True)
        confirm = str(raw_input("run test again ? "))
        if confirm != "n":
           # reregister
           pass
        

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork(sys.argv[1],sys.argv[2],sys.argv[3])

