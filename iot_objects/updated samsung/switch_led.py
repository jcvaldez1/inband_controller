from gpiozero import LED
from gpiozero import Button
from time import sleep
import requests
import json
import datetime

led = LED(2)
button = Button(3)
prev=0
curr=0
print("in")

curr_seq_num = 0

while True:
    if button.is_pressed:
        curr=1
        curr_seq_num += 1
        if prev != curr:
            data = {'deviceID':'RPI',
                    'signal':'on',
                    'sequence_num': curr_seq_num,
                    'group': '1'
                }
            led.on()
            print("preon")
            
            try:
                requests.post(url = 'http://52.74.73.81/report', json = data, timeout = 5)
                print("on")
                print(datetime.datetime.now())

                curr_time = datetime.datetime.now()
                ts = str(curr_time) + " ON"
                time_log = open("switch_log.txt", "a")
                time_log.write(ts)
                time_log.close()

            except Exception as e:
                print(e)
                pass
            
            prev = curr
            
    else:
        curr=0
        curr_seq_num += 1
        if prev != curr:
            data = {'deviceID':"RPI",
                    'signal':"off",
                    'sequence_num': curr_seq_num,
                    'group': '1'
                }
            led.off()
            try:
                requests.post(url = 'http://52.74.73.81/report', json = data,  timeout = 5)
                print("off")

                curr_time = datetime.datetime.now()
                ts = str(curr_time) + " OFF"
                time_log = open("switch_log.txt", "a")
                time_log.write(ts)
                time_log.close()
            except:
                print("post fail")
                pass
            prev = curr
            
    sleep(1)
