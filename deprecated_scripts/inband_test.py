#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.link import Link, TCLink

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( topo=None,
                   build=False)

    net.addController( 'c0',
                       controller=RemoteController,
                       ip='127.0.0.1'  )

    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )

    s1 = net.addSwitch( 's1', cls=OVSSwitch )

    #net.addLink( h1, s1 )
    net.addLink( h2, s1 )
    Link(h1, s1, intfName1='h1-eth0')
    Link(h1, s1, intfName1='h1-eth1')
    h1.cmd('ifconfig h1-eth1 10.0.10.1 netmask 255.255.255.0')


    net.start()

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
