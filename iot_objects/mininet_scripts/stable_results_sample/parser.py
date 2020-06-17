import datetime
import statistics

def parse_log_line(logline):
    buffer = logline.split()
    #return {'seq':buffer[3],'time':buffer[1]}
    # seq : time
    return {buffer[3]:buffer[1]}

def list_plusser(timedelta_list):
    # because sum() doesnt work for
    # non ints for some reason
    sum_ret = datetime.timedelta()
    for x in timedelta_list:
        sum_ret += x
    return sum_ret
        

#host_ct = int(input('input number of hosts'))

min_delay = datetime.timedelta.max
max_delay = datetime.timedelta.min
truncator = datetime.timedelta(minutes=10)
total_seqs = 0
ave_delay = 0
delay_list = []
losses = []

for host_n in range(2,200):
    if host_n % 2 == 0:
             actuator_file = open('./actuator/'+str(host_n)+'_actuator_log.log','r')
             receiver_file = open('./receiver/'+str(host_n+1)+'_receiver_log.log','r')
             ac_lines = actuator_file.readlines()
             rc_lines = receiver_file.readlines()
             actuator_file.close()
             receiver_file.close()
             ac_lines_parsed = {}
             rc_lines_parsed = {}
             for line in ac_lines:
                 ac_lines_parsed = {**ac_lines_parsed, **parse_log_line(line)}
             for line in rc_lines:
                 rc_lines_parsed = {**rc_lines_parsed, **parse_log_line(line)}

             for seq in rc_lines_parsed:
                 ac_time = datetime.datetime.strptime(ac_lines_parsed[seq],'%H:%M:%S.%f')
                 rc_time = datetime.datetime.strptime(rc_lines_parsed[seq],'%H:%M:%S.%f')
                 delay = rc_time-ac_time
                 delay_list.append(delay)
                 if delay < min_delay:
                     min_delay = delay
                 elif delay > max_delay:
                     max_delay = delay
             total_seqs += len(rc_lines_parsed)
             losses.append(int(len(ac_lines_parsed)) - int(len(rc_lines_parsed)))
             #print(str(host_n)+","+str(host_n+1)+" pair : "+str(len(rc_lines_parsed)))

print("min delay : "+str(min_delay))
print("max delay : "+str(max_delay))
print("ave delay : "+str(list_plusser(delay_list)/total_seqs))

try:
    print("mean losses : " + str(statistics.mean(losses)))
    print("median losses : " + str(statistics.median(losses)))
    print("mode losses : " + str(statistics.mode(losses)))
except:
    pass
