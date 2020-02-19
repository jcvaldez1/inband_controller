import json

id_count = int(input('input number of device IDs'))
out = open('configs.txt','w')





buffer = []
for c_id in range(0,id_count):
    if c_id % 2 == 0:
        fwd_rule = {"commandID":"actuatorFWD_"+str(c_id),"commandDetails":{"group":1,"deviceID":c_id,"targetIP":"http://13.55.147.2/report","signal":"any","commType":"forward"}}
        buffer.append(json.dumps(fwd_rule, sort_keys=True, indent=4))
        buffer.append('\n\n')
    else:
        off_rule = {"commandID":"deviceOFF_"+str(c_id),"commandDetails":{"group":1,"deviceID":c_id-1,"signal":"OFF","commType":"device"}}
        on_rule = {"commandID":"deviceON_"+str(c_id),"commandDetails":{"group":1,"deviceID":c_id-1,"signal":"ON","commType":"device"}}    
        buffer.append(json.dumps(on_rule, sort_keys=True, indent=4))
        buffer.append('\n\n')
        buffer.append(json.dumps(off_rule, sort_keys=True, indent=4))
        buffer.append('\n\n')
out.writelines(buffer)