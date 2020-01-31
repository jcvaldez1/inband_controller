from time import sleep
import requests
import json
import datetime

curr_seq_num = 0
num_iterations = 20
sleep_interval = 0.1

for i in range(0, num_iterations):
    if i%2 == 0:
        try:
            curr_time = datetime.datetime.now()
            ts = str(curr_time) + " ON " + str(curr_seq_num)
            time_log = open("switch_log.txt", "a")
            time_log.write(ts + '\n')
            time_log.close()
            data = {'deviceID':'RPI',
                    'signal':'on',
                    'sequence_num': curr_seq_num,
                    'group': '1'
                }
            requests.post(url = 'http://52.74.73.81/report', json = data, timeout = 5)
            print("on")
            print(datetime.datetime.now())
            
            curr_seq_num += 1

        except Exception as e:
            print(e)
            pass
    else:
        try:
            curr_time = datetime.datetime.now()
            ts = str(curr_time) + " OFF " + str(curr_seq_num)
            time_log = open("switch_log.txt", "a")
            time_log.write(ts + '\n')
            time_log.close()
            data = {'deviceID':"RPI",
                    'signal':"off",
                    'sequence_num': curr_seq_num,
                    'group': '1'
                }
            
            requests.post(url = 'http://52.74.73.81/report', json = data,  timeout = 5)
            print("off")
            
            curr_seq_num += 1

        except:
            print("post fail")
            pass
        
    sleep(sleep_interval)