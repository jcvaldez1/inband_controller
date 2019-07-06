# !/bin/bash/python3
import sys
import time
import shlex
import datetime
sys.path.insert(0, "/home/wang/physical2/working_model/")

#import constants

def myTest(net): 
    hosts = net.hosts
    print "Starting test..."
    popens = {}
    # ONLY THE FIRST HOST WOULD BE THE CLIENT
    hosts[0].popen("tshark -w ./testresults.pcap -i 'h1-eth0' -a duration:180")
    popens[hosts[1]] = hosts[1].popen("python3 ./server.py 2")
    popens[hosts[2]] = hosts[2].popen("python3 ./server.py 3")
    popens[hosts[3]] = hosts[3].popen("python3 ./server.py 4")
    popens[hosts[0]] = hosts[0].popen('python3', "./client_script.py")
    # RUN SERVER CODE ON REMAINING HOSTS

    #hosts[0].setIP('192.168.145.44')
    #hosts[1].setIP('192.168.145.45')
    #for h in hosts:
        # HOSTS ARE IN ORDER OF ADDITION
        # if h.IP() == '192.168.145.44':
        #if h.IP() == '10.0.0.1':
        #    #print(h.cmd("cd " + constants.MODEL_PATH + "; source /ndsg-model/bin/activate;" + " python3 ~/physical2/working_model/server_starter.py"))
        #    #command = "cd " + constants.MODEL_PATH + "; source /ndsg-model/bin/activate;" + " python3 ~/physical2/working_model/server_starter.py"
        #    popens[h] = h.popen('python3', constants.SERVER_SCRIPT_PATH)
        #    #popens[h] = h.popen(shlex.split(command))
        #    # print("server_start!!! " + str(h.cmd('ifconfig')))
        #    print("Monitoring output for 10 seconds")
        #    time.sleep(5)
        #else:
        #    print(h.cmd('python3 ~/physical2/working_model/test_client.py'))
        #    pass

    time.sleep(180)


tests = { 'mytest': myTest }
