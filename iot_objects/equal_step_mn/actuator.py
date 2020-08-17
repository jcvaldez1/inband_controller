from time import sleep
import requests
import json
import datetime
import sys
import makedir
import threading
import subprocess

if len(sys.argv) < 5:
    print("Usage: python3 actuator.py <iterations> <sleep_interval> <host_number> <actuator_cloud_ip>")
    sys.exit(1)

num_iterations = sys.argv[1]
sleep_interval = sys.argv[2]
host_name      = sys.argv[3]
samsung_ip     = sys.argv[4]
starting_num   = sys.argv[5]

import threading

# Function for sending HTTP post request
def post_sender(state, data):
    res = requests.post(url = 'http://'+samsung_ip+'/report', json = data, timeout = 60)
    print(state + str(res))
    return

"""
    logs time to file
    filename    :   log file filename
    state       :   "ON" / "OFF"
"""
def log_result(filename, state, curr_seq):
    curr_time = datetime.datetime.now()
    ts = str(curr_time) + " " + state + " " + str(curr_seq)
    with makedir.safe_open_w(filename) as time_log:
        time_log.write(ts + '\n')
        time_log.close()

if __name__ == "__main__":
    threads = []
    for i in range(int(starting_num), int(starting_num)+int(num_iterations)):
        try:
            state = "ON" if (i % 2 == 0) else "OFF"
            data = { 'deviceID':str(host_name),
                     'signal':state,
                     'sequence_num': i,
                     'group': '1'  }
            #log_result("./temp_act/actuator/"+str(samsung_ip)+"/"+str(host_name)+ "_actuator.log", state, i)
            log_result("./results/actuator/"+str(samsung_ip)+"/"+str(host_name)+ "_actuator.log", state, i)
            #subprocess.Popen(["python3" ,"post_sender.py" ,samsung_ip ,json.dumps(data)])
            ip_use = 'http://' + samsung_ip +'/report'
            subprocess.Popen(["curl" ,"-X" ,"POST" 
                                     ,"-H" ,"Content-Type: application/json" 
                                     ,"-d" ,json.dumps(data) ,ip_use])
            #log_result("./temp_act/actuator/"+str(samsung_ip)+"/"+str(host_name)+ "_actuator.log", "THREAD DONE", i)
        except Exception as e:
            print(e)
        sleep(float(sleep_interval))
