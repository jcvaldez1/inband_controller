import socket
import random
import json
from time import sleep
import time
import sys

def send_dummy(data=None):
    UDP_IP_ADDRESS = "69.4.20.69"
    UDP_PORT_NO = 420
    print(data)
    data_json = json.dumps(data)
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto(bytes(data_json,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    file = open("ghost_reglog.txt", "a")
    file.write(str(time.time()) + "\n")
    file.close()

def lifx_data(ip_mod):
    id_modifier = str((ip_mod%255)+1)
    data = {
        'device_id':random.getrandbits(16),
        'name': "Lifx_"+id_modifier,
        'ports':[80,42915],
        #'cloud_ip': "13.55.147.2",
        'cloud_ip': "13.55.147."+id_modifier,
        'user_id': 1
    }
    return data
    
def samsong_data(ip_mod):
    id_modifier = str((ip_mod%255)+1)
    data = {
        'device_id':random.getrandbits(16),
        'name': "samsong_"+id_modifier,
        'ports':[80,42915],
        #'cloud_ip': "52.74.73.81",
        'cloud_ip': "52.74.73."+id_modifier,
        'user_id': 1
    }
    return data
    



def dummy_registration(host_num):
    for x in range(0,host_num):
        if x%2 == 0:
            #print(lifx_data(x))
            send_dummy(lifx_data(x))
        else:
            #print(samsong_data(x))
            send_dummy(samsong_data(x))
        sleep(5)
    

if __name__ == "__main__":
    host_num = int(sys.argv[1])
    dummy_registration(host_num)
