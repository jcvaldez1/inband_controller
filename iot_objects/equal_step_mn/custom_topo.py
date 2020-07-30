#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info
import subprocess
import datetime
import sys

# kill all python processses runnning
def kill_all_py(hosts):
    ps_string = subprocess.check_output(["ps","-ef"]).split("\n")
    pid_string = [x for x in ps_string if ("python" in x)]
    print(pid_string)
    for x in pid_string:
       if not ("custom_topo" in x):
          stringy = filter(None, x.split(" "))[1]
          hosts[0].cmdPrint("kill "+str(stringy))

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
    Intf( 'enp2s0', node=s1 )

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
    max_count = int(raw_input("perform on how many container pairs? "))
    request_num = int(raw_input("numbers of request? "))
    while confirm != "n":
        current_request = 0
        container_counter = 0
        for x in range(0, host_num):
            
            # move on to the next container pair
            if x/max_id > container_counter:
                container_counter += 1
            # limit the container pairs involved
            if container_counter >= max_count:
                 break

            # spin up the IoT device scripts
            if x % 2 == 0:
                cmdstring = "python3 actuator.py "+str(request_num)+" 0.5 "+ str(x%max_id)+ " 52.74.73."+str((container_counter*2)+2) + " "+ str(current_request)
                current_request = current_request + request_num + 1
            else:
                cmdstring = "python receiver.py "+str((x%max_id))+ " 13.55.147."+str((container_counter*2)+1)
            hosts[x].cmdPrint(cmdstring+" &")

        raw_input("parse results? ")
        
        # kill all python processes
        kill_all_py(hosts)

        # save results
        curr_time = str(datetime.datetime.now().strftime("%H:%M:%S"))
        cmd_list = "./results_mover.sh "+str(max_id)+" "+ curr_time+" "+str(container_number)
        subprocess.call(cmd_list, shell=True)
        
        # reset variables
        confirm = str(raw_input("run test again ? "))
        if confirm != "n":
           if str(raw_input("same values ? ")) == "n":
              container_number = int(raw_input("container number ? "))
              hosts[0].cmdPrint("sudo python3 ./ghost_reg.py "+str(container_number))
              container_split = 100/int(raw_input("container split %? "))
              max_id = host_num/container_split
              max_count = int(raw_input("perform on how many container pairs? "))
              request_num = int(raw_input("numbers of request? "))
              raw_input("configs done ? ")
              

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork(sys.argv[1],sys.argv[2],sys.argv[3])

