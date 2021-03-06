import json
import requests
import sys

devices=int(sys.argv[1])
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
                                         ,"targetIP" : "http://13.55.147.2/report"
                                         ,"signal"   : "any"
                                         ,"commType" : "forward" 
                                        }
                   }
        sensor_configs.append(fwd_rule)
        #buffer.append(json.dumps(fwd_rule, sort_keys=True, indent=4))
        #buffer.append('\n\n')

    # FOR ACTUATOR DEVICES 13.55.147.2
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
        #buffer.append(json.dumps(on_rule, sort_keys=True, indent=4))
        #buffer.append('\n\n')
        #buffer.append(json.dumps(off_rule, sort_keys=True, indent=4))
        #buffer.append('\n\n')
    #out.writelines(buffer)

#for config in sensor_configs:
#    #requests.post("http://52.74.73.81/config", json=config)
#    requests.post("http://"+sys.argv[2]+"/config", json=config)

for config in actuator_configs:
    requests.post("http://"+sys.argv[3]+"/config", json=config)

