from time import sleep
import json
import sys
import subprocess

if len(sys.argv) < 5:
    print("Usage: python3 actuator.py <iterations> <sleep_interval> <host_number> <actuator_cloud_ip>")
    sys.exit(1)

num_iterations = sys.argv[1]
sleep_interval = sys.argv[2]
host_name      = sys.argv[3]
samsung_ip     = sys.argv[4]
starting_num   = sys.argv[5]


if __name__ == "__main__":
    for i in range(int(starting_num), int(starting_num)+int(num_iterations)):
        try:
            state = "ON" if (i % 2 == 0) else "OFF"
            data = { 'deviceID':str(host_name),
                     'signal':state,
                     'sequence_num': i,
                     'group': '1'  }
            ip_use = 'http://' + samsung_ip +'/report'
            subprocess.Popen(["curl" ,"-X" ,"POST" 
                                     ,"-H" ,"Content-Type: application/json" 
                                     ,"-d" ,json.dumps(data) ,ip_use])
        except Exception as e:
            print("dfdF")
            #print(e)
        sleep(float(sleep_interval))
