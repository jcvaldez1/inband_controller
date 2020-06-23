from time import sleep
import requests
import json
import datetime
import sys

if len(sys.argv) < 5:
    print("Usage: python3 actuator.py <iterations> <sleep_interval> <host_number> <actuator_cloud_ip>")
    sys.exit(1)

num_iterations = sys.argv[1]
sleep_interval = sys.argv[2]
host_name      = sys.argv[3]
samsung_ip     = sys.argv[4]


"""
    logs time to file
    filename    :   log file filename
    state       :   "ON" / "OFF"
"""
def log_result(filename, state, curr_seq):
    curr_time = datetime.datetime.now()
    ts = str(curr_time) + " " + state + " " + str(curr_seq)
    with open(filename, "a+") as time_log:
        time_log.write(ts + '\n')
        time_log.close()

if __name__ == "__main__":

    for i in range(0, int(num_iterations)):
        try:
            state = "ON" if (i % 2 == 0) else "OFF"
            data = { 'deviceID':str(host_name),
                     'signal':state,
                     'sequence_num': i,
                     'group': '1'  }
            log_result("./results/actuator/"+str(host_name) + "_" + str(samsung_ip) + "_actuator_log.log", state, i)
            res = requests.post(url = 'http://'+samsung_ip+'/report', json = data, timeout = 5)
            print(state + str(res))
        except Exception as e:
            print(e)
            pass
        sleep(float(sleep_interval))
