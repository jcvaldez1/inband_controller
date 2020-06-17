import datetime
import statistics
import sys

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

def parse_results(host_count, filename):
    host_ct = int(host_count)
    fname = str(filename)
    
    min_delay = datetime.timedelta.max
    max_delay = datetime.timedelta.min
    delay_cutoff = datetime.timedelta(minutes=10)
    total_seqs = 0
    ave_delay = 0
    delay_list = []
    losses = []
    output_file = open('experiments/'+fname+'/results','w+')
    
    for host_n in range(2,host_ct):
        if host_n % 2 == 0:
           try:
                 actuator_file = open('experiments/'+fname+'/actuator/'+str(host_n)+'_actuator_log.log','r')
                 receiver_file = open('experiments/'+fname+'/receiver/'+str(host_n+1)+'_receiver_log.log','r')
                 ac_lines = actuator_file.readlines()
                 rc_lines = receiver_file.readlines()
                 ac_lines_parsed = {}
                 rc_lines_parsed = {}
                 actuator_file.close()
                 receiver_file.close()
                 overtime_count = 0
                 for line in ac_lines:
                     ac_lines_parsed = {**ac_lines_parsed, **parse_log_line(line)}
                 for line in rc_lines:
                     rc_lines_parsed = {**rc_lines_parsed, **parse_log_line(line)}
    
                 for seq in rc_lines_parsed:
                     ac_time = datetime.datetime.strptime(ac_lines_parsed[seq],'%H:%M:%S.%f')
                     rc_time = datetime.datetime.strptime(rc_lines_parsed[seq],'%H:%M:%S.%f')
                     ms_delay = rc_time-ac_time
                     if ms_delay <= delay_cutoff:
                        delay_list.append(ms_delay)
                        if ms_delay < min_delay:
                            min_delay = ms_delay
                        if ms_delay > max_delay:
                            max_delay = ms_delay
                     else:
                        overtime_count += 1

                 actual_responses = len(rc_lines_parsed) - overtime_count
                 total_seqs += actual_responses
                 losses.append(int(len(ac_lines_parsed)) - int(len(rc_lines_parsed)) + overtime_count)
                 output_file.write(str(host_n)+","+str(host_n+1)+" pair : "+str(actual_responses)+"\n")
           except:
                 pass
    try:
        output_file.write("mean losses : " + str(statistics.mean(losses))+"\n")
        output_file.write("median losses : " + str(statistics.median(losses))+"\n")
        output_file.write("mode losses : " + str(statistics.mode(losses))+"\n")
    except:
        pass
    output_file.write("min delay : "+str(min_delay)+"\n")
    output_file.write("max delay : "+str(max_delay)+"\n")
    output_file.write("ave delay : "+str(list_plusser(delay_list)/total_seqs)+"\n")
    output_file.close()

if __name__ == "__main__":
    parse_results(sys.argv[1], sys.argv[2])
    
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
