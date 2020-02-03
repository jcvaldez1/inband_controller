import socket
import random
import json
from time import sleep import time

def send_dummy(brand_name, ip_addr, data=None):
    UDP_IP_ADDRESS = "69.4.20.69"
    UDP_PORT_NO = 420

    print(data)
    data_json = json.dumps(data)
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto(bytes(data_json,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    file = open("ghost_reglog.txt", "a")
    file.write(str(time.time()) + "\n")
    file.close()

def samsong_dummy_registration():
    ip_addr = "13.55.147.2"
    data = {
        'device_id':random.getrandbits(16)
        'ports':[80,42915],
        'name': "Lifx",
        'cloud_ip': ip_addr
        'user_id': 1
    }
    send_dummy(None, None, data)
    ip_addr = "52.74.73.81"
    data["name"] = "samsong"
    data["cloud_ip"] = ip_addr
    data["user_id"] = 2
    sleep(5)
    send_dummy(None, None, data)
    

if __name__ == "__main__":
    num_of_devs = int(input("Enter number of devices: "))
    uniqueness = input("Unique brands? (y/n): ")
    ip1 = 0
    ip2 = 0
    ip3 = 0
    ip4 = 0
    samsong_dummy_registration()
