#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info
import subprocess
import datetime

def myNetwork():
    hosts = [];
    host_num = 100
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
    

    while confirm != "n":
        for x in range(2, host_num):
            if x % 2 == 0:
                cmdstring = "python3 actuator.py 1000 0.5 "+ str(x)
            else:
                cmdstring = "python receiver.py "+str(x)
            hosts[x].cmdPrint(cmdstring+" &")

        raw_input("parse results? ")
        ps_string = subprocess.check_output(["ps","-ef"]).split("\n")
        pid_string = [x for x in ps_string if ("python" in x)]
        print(pid_string)
        for x in pid_string:
           if not ("custom_topo" in x):
              stringy = filter(None, x.split(" "))[1]
              hosts[0].cmdPrint("kill "+str(stringy))

        # parse results
        cmd_list = "./results_mover.sh "+str(host_num) +" "+str(datetime.datetime.now().strftime("%H:%M:%S"))
        subprocess.call(cmd_list, shell=True)
        # UNDER TESTING
        confirm = str(raw_input("run test again ? "))
        

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

