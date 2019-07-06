import net_elements
import socket
import constants
import subprocess
import ast


# FOR NOW THE IP IS SET HERE, BUT THIS SHOULD BE SET TO 
# THE RESPECTIVE IP OF THE HOST AT THE h1-eth0 INTERFACE
# (OR THE INTERFACE CONNECTED TO THE MAIN SWITCH)
my_ip = "10.0.0.2"


# WRAPPER THAT RUNS THE REQUEST NATURE SCRIPT
# ALL THIS BLOCK DOES IS RUN THE SCRIPT IN
# PYTHON2 DUE TO DEPENDENCY ISSUES ON SCAPY

python_command = ['python','test_packets.py',constants.PCAP_FILE_NAME]
proc = subprocess.Popen(python_command,stdout=subprocess.PIPE)
list_packets = proc.stdout.read()
list_packets = list_packets.decode()
list_packets_new = list_packets[:len(list_packets)-1]
list_packets = ast.literal_eval(list_packets_new)

# PYTHON2 WRAPPER BLOCK ENDS HERE
# THANK YOU AND HAVE A NICE DAY

raw_data = list_packets
# RAW_DATA OUTPUT
#         pay     delay time       resp      src_ip            dst_ip   conn_ender
# ('TCP', 58, 0.003567868470993611, 42, ('10.147.80.139', '10.16.5.225'), 0)

is_server = False
for x in raw_data:
    # CHECK IF THIS HOST IS PART OF THE DESTINATIONS
    index = x[4][1]
    if index == my_ip:
        is_server = True

if is_server:
    # starts the server up
    this_server = net_elements.Server(my_ip)
    this_server.start_socket()
    
else:
    print("SERVER DOESNT HAVE IP AS A DESTINATION!")
    # TEMPORARY FIX DONT REMOVE UNTIL
    # MININET HOST IP CAN BE CONFIGURED
    this_server = net_elements.Server(address=my_ip)
    this_server.start_socket()






