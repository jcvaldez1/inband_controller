#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info

def myNetwork():
    hosts = [];
    net = Mininet( topo=None,
                   build=False, controller = OVSController)

    info( '*** Adding controller\n' )
    net.addController(name='c0')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    Intf( 'eno2', node=s1 )

    info( '*** Add hosts\n')
    
    h1 = net.addHost('h1', ip='0.0.0.0')
    h2 = net.addHost('h2', ip='0.0.0.0')
    h3 = net.addHost('h3', ip='0.0.0.0')
    h4 = net.addHost('h4', ip='0.0.0.0')

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    info( '*** Starting network\n')
    net.start()
    h1.cmdPrint('dhclient '+h1.defaultIntf().name)
    h2.cmdPrint('dhclient '+h2.defaultIntf().name)
    h3.cmdPrint('dhclient '+h3.defaultIntf().name)
    h4.cmdPrint('dhclient '+h4.defaultIntf().name)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

