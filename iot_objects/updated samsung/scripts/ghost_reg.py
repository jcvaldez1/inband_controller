import socket
import json

from time import sleep

def send_dummy(brand_name, ip_addr):
    UDP_IP_ADDRESS = "69.4.20.69"
    UDP_PORT_NO = 420

    data = {
        #'ports':[6,9],
        'name': brand_name,
        'cloud_ip': ip_addr
    }

    data_json = json.dumps(data)

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto(bytes(data_json,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))

if __name__ == "__main__":
    num_of_devs = int(input("Enter number of devices: "))
    uniqueness = input("Unique brands? (y/n): ")
    ip1 = 1
    ip2 = 0
    ip3 = 0
    ip4 = 0

    if uniqueness == "y":
        for i in range(1000, num_of_devs):
            brand_name = "brand" + str(i)

            ip4 += 1

            if ip4 > 255:
                ip3 += 1
                ip4 = 0
            if ip3 > 255:
                ip2 += 1
                ip3 = 0
            if ip2 > 255:
                ip1 += 1
                ip2 = 0

            ip_addr = str(ip1) + "." + str(ip2) + "." +  str(ip3) + "." + str(ip4)
            print(ip_addr)
            send_dummy(brand_name,ip_addr)
            sleep(5)
    else:
        for i in range(0, num_of_devs):
            send_dummy("brand0", '69.4.20.69')
            sleep(5)
        
