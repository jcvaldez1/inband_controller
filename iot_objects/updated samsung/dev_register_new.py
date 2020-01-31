import socket
import json
import requests

def enroll():
    enroll_data = json.dumps({'group':'debug','device_ID':'debug'})
    temp = requests.post(url = 'http://13.55.147.2/enroll', json = enroll_data, timeout = 5)
    print(temp.text)

def send_dummy():
    print("in")
    UDP_IP_ADDRESS = "69.4.20.69"
    UDP_PORT_NO = 420
    
    data = {
        #'ports': {'80/tcp': 6,'42915/tcp': 9},
        'name': 'samsung',
        'cloud_ip': '42915'
    }

    data_json = json.dumps(data)

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto(bytes(data_json,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))

if __name__ == "__main__":
    enroll()
    send_dummy()