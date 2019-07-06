from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController
import sys
import time
import shlex
import datetime

class InbandController( RemoteController ):

    def checkListening( self ):
        "Overridden to do nothing."
	pass
        #return True


class MyTopo( Topo ):
    "Simple topology example."

    #def __init__( self ):
    def build(self):
        "Create custom topo."

        # Initialize topology
        #Topo.__init__( self )

        # Add hosts and switches

        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        host3 = self.addHost( 'h3' )
        host4 = self.addHost( 'h4' )
        cont1 = self.addHost( 'h5' )
        s1 = self.addSwitch( 's1', cls=OVSSwitch )
        s2 = self.addSwitch( 's2', cls=OVSSwitch )

        # Add links
        self.addLink( host1, s1 )
        self.addLink( s1, host2 )
        self.addLink( host3, s2 )
        self.addLink( s2, host4 )
        self.addLink( s2, s1 )
        self.addLink( cont1, s1 )
        self.addLink( s2, cont1 )

if __name__ == '__main__':
    setLogLevel('info')
    topo = MyTopo()
    
    #c1 = RemoteController('cont1', ip='10.0.0.5')
    #c1 = InbandController('c1', ip='127.0.0.1')
    c1 = RemoteController('c1', ip='127.0.0.1')
    #c1 = RemoteController('c1', ip='10.0.0.5')
    net = Mininet(topo=topo, controller=c1)
    #net = Mininet(topo=topo, controller=None)
    #net = Mininet( topo=None,
                   build=False,controller=None)
    #net = Mininet(topo)

    #net = Mininet(topo=None, build=False)
    #host1 = net.addHost( 'h1' )
    #host2 = net.addHost( 'h2' )
    #host3 = net.addHost( 'h3' )
    #host4 = net.addHost( 'h4' )
    #cont1 = net.addHost( 'h5' )
    #s1 = net.addSwitch( 's1', cls=OVSSwitch, inNamespace=True )
    #s2 = net.addSwitch( 's2', cls=OVSSwitch, inNamespace=True )

    ## Add links
    #net.addLink( host1, s1 )
    #net.addLink( s1, host2 )
    #net.addLink( host3, s2 )
    #net.addLink( s2, host4 )
    #net.addLink( s2, s1 )
    #net.addLink( cont1, s1 )
    #net.addLink( s2, cont1 )

    hosts = net.hosts
    #hosts[4].popen("ryu-manager controller.py")
    #net.addController('cont1', controller=RemoteController, ip='10.0.0.5')

    #net.addController('cont1', controller=RemoteController, ip='127.0.0.1')

    net.start()
    #CLI(net)
    time.sleep(5)

    print("ADDING CONTROLLER")
    #net.addController('c0', controller=RemoteController, ip='127.0.0.1')
    time.sleep(5)

    print("PINGING ALL")
    net.pingAll()

    print("Starting test...")
    popens = {}
    hosts[0].popen("sudo tshark -w ./testresults.pcap -a duration:100")
    popens[hosts[1]] = hosts[1].popen("python3 ./server.py 2")
    popens[hosts[2]] = hosts[2].popen("python3 ./server.py 3")
    popens[hosts[3]] = hosts[3].popen("python3 ./server.py 4")
    popens[hosts[0]] = hosts[0].popen('python3', "./client_script.py")
    #CLI(net)
    #print("POST CLI BOY")
    time.sleep(30)
    net.configLinkStatus('s1','h2','down')

    time.sleep(20)
    net.configLinkStatus('s2','h3','down')

    time.sleep(20)
    net.configLinkStatus('s2','h3','up')

    time.sleep(20)
    net.configLinkStatus('s1','h2','up')
    time.sleep(20)
    print("ending test")
    net.stop()


#tests = { 'mytest': myTest }
#
#topos = { 'mytopo': ( lambda: MyTopo() ) }

