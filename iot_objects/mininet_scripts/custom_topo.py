#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info

def myNetwork():
    hosts = [];
    host_num = 30
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
    #CLI(net)

    for x in range(0, host_num):
        if x % 2 == 0:
            cmdstring = "python3 actuator.py 100 0.5 "+ str(x)
        else:
            cmdstring = "python receiver.py "+str(x)
        hosts[x].cmdPrint(cmdstring+" &")

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

