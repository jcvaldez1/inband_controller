import json
import requests
import sys




def generate_config(devices, offset):
    sensor_configs = []
    actuator_configs = []
    for c_id in range(0, devices):

        # FOR SENSOR DEVICES 52.
        if c_id % 2 == 0:
            fwd_rule = { 
                         "commandID"      : "actuatorFWD_"+str(c_id)
                        ,"commandDetails" : { 
                                              "group"    : 1
                                             ,"deviceID" : str(c_id)
                                             ,"targetIP" : "http://13.55.147."+str(offset)+"/report"
                                             ,"signal"   : "any"
                                             ,"commType" : "forward" 
                                            }
                       }
            sensor_configs.append(fwd_rule)
        # FOR ACTUATOR DEVICES 13.55.147.X
        else:
            off_rule = { 
                         "commandID"      :   "deviceOFF_"+str(c_id)
                        ,"commandDetails" : { 
                                              "group"    : 1
                                             ,"deviceID" : str(c_id-1)
                                             ,"target"   : str(c_id)
                                             ,"signal"   : "OFF" 
                                             ,"commType" : "device"
                                             ,"sayThis"  : "OFF"
                                            } 
                       }
            actuator_configs.append(off_rule)
            on_rule  = { 
                         "commandID"      :   "deviceON_"+str(c_id)
                        ,"commandDetails" : { 
                                              "group"    : 1
                                             ,"deviceID" : str(c_id-1)
                                             ,"target"   : str(c_id)
                                             ,"signal"   : "ON"
                                             ,"commType" : "device"
                                             ,"sayThis"  : "ON"
                                            }
                       }    
            actuator_configs.append(on_rule)
    return sensor_configs, actuator_configs


def send_configs(config_list, ip_port):
    for config in config_list:
        requests.post("http://"+str(ip_port)+"/config", json=config)

if __name__ == "__main__":
    devices = int(sys.argv[1])
    # split of devices into containers 5 for 1/5, 4 for 1/4
    container_split = int(sys.argv[2])
    start_port = int(sys.argv[3])
    ddh_ip = str(sys.argv[4])
    # send configs
    for x in range(0,container_split):
        sensor_configs, actuator_configs = generate_config(int(devices/container_split),(x*2)+1)
        send_configs(actuator_configs, ddh_ip+":"+str(start_port))
        send_configs(sensor_configs, ddh_ip+":"+str(start_port+2))
        start_port += 4
    
