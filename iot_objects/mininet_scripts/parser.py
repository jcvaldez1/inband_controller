import datetime
import statistics
import sys

def parse_log_line(logline):
    buffer = logline.split()
    #return {'seq':buffer[3],'time':buffer[1]}
    # seq : time
    return {buffer[3]:buffer[1]}

#output_file = open('output.txt','w')

#host_ct = int(input('input number of hosts'))
host_ct = int(sys.argv[1])

min_delay = 1000
max_delay = 0
total_seqs = 0
ave_delay = 0
delay_list = []
losses = []

for host_n in range(0,host_ct):
    if host_n % 2 == 0:
        try:
             host_pair_buffer = []
             host_pair_buffer.append('---actuator '+str(host_n)+' and '+'receiver '+str(host_n+1)+'---\n')
             actuator_file = open('experiments/results/actuator/'+str(host_n)+'_actuator_log.log','r')
             receiver_file = open('experiments/results/receiver/'+str(host_n+1)+'_receiver_log.log','r')
             #actuator_file = open(str(host_ct)+'_host_strong/results/actuator/'+str(host_n)+'_actuator_log.log','r')
             #receiver_file = open(str(host_ct)+'_host_strong/results/receiver/'+str(host_n+1)+'_receiver_log.log','r')
             ac_lines = actuator_file.readlines()
             rc_lines = receiver_file.readlines()
             ac_lines_parsed = {}
             rc_lines_parsed = {}
             for line in ac_lines:
                 ac_lines_parsed = {**ac_lines_parsed, **parse_log_line(line)}
             for line in rc_lines:
                 rc_lines_parsed = {**rc_lines_parsed, **parse_log_line(line)}

             for seq in rc_lines_parsed:
                 ac_time = datetime.datetime.strptime(ac_lines_parsed[seq],'%H:%M:%S.%f')
                 rc_time = datetime.datetime.strptime(rc_lines_parsed[seq],'%H:%M:%S.%f')
                 ms_delay = (rc_time-ac_time).microseconds/1000
                 delay_list.append(ms_delay)
                 if ms_delay < min_delay:
                     min_delay = ms_delay
                 elif ms_delay > max_delay:
                     max_delay = ms_delay
                 #print(ms_delay)
                 #host_pair_buffer.append(str(ms_delay)+'\n')
             total_seqs += len(rc_lines_parsed)
             losses.append(100 - int(len(rc_lines_parsed)))
             print(str(host_n)+","+str(host_n+1)+" pair : "+str(len(rc_lines_parsed)))
             #output_file.writelines(host_pair_buffer)
        except:
             pass 

try:
    print("mean losses : " + str(statistics.mean(losses)))
    print("median losses : " + str(statistics.median(losses)))
    print("mode losses : " + str(statistics.mode(losses)))
except:
    pass
print("min : "+str(min_delay))
print("max : "+str(max_delay))
print("ave : "+str(sum(delay_list)/total_seqs))

#output_file.close()
#
#input_file = open('output.txt','r')
#output_file = open('results.tsv','w')
#
#write = ""
#for line in input_file:
#    l = line.split()
#    if(l[0] == '---actuator'):
#        output_file.writelines(write + "\n")
#        write = "sw" + l[1] + " act" + l[4]
#    else:
#        write = write + "\t" + l[0]
#output_file.writelines(write)
