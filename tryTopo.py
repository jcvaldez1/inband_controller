#!/usr/bin/python

from mininet.net import Mininet, MininetWithControlNet
from mininet.node import RemoteController, OVSSwitch, Controller, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class InbandController( RemoteController ):

    def checkListening( self ):
        "Overridden to do nothing."
        return

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( topo=None,
                   build=False,controller=None)


    h1 = net.addHost( 'h1', ip='10.0.0.1')
    h2 = net.addHost( 'h2', ip='10.0.0.2')
    h3 = net.addHost( 'h3', ip='10.0.0.3')

    s1 = net.addSwitch( 's1', cls=UserSwitch, inNamespace=True )
    s2 = net.addSwitch( 's2', cls=UserSwitch, inNamespace=True )

    h1s1=net.addLink( h1, s1 )
    net.addLink( h2, s1 )
    s1s2=net.addLink( s1, s2 )
    net.addLink( h3, s2 )

    net.start()
    # Set default route in host running controller
    h1.setDefaultRoute('dev h1-eth0')
    # Set the mgmt IP address of the switches
    #s1.cmd('ifconfig lo 11.0.0.1/32')
    #s2.cmd('ifconfig lo 11.0.0.2/32')
    # Set the route in each switch to the location of the controller.
    # This is brute force static routes.  Maybe OSPF or ISIS would be better.
    s1ctrl=None
    if (s1 == h1s1.intf1.node):
       s1ctrl=h1s1.intf1
    else:
       s1ctrl=h1s1.intf2
    s1.setHostRoute('10.0.0.1', s1ctrl)

    s2ctrl=None
    if (s2 == s1s2.intf1.node):
       s2ctrl=s1s2.intf1
    else:
       s2ctrl=s1s2.intf2
    s2.setHostRoute('10.0.0.1', s2ctrl)
    net.addController( 'c0', 
                       controller=InbandController, 
                       ip='10.0.0.1'
                       )

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()

