import datetime
import statistics
import sys
import traceback

def parse_log_line(logline):
    buffer = logline.split()
    #return {'seq':buffer[3],'time':buffer[1]}
    # seq : time
    return {buffer[3]:buffer[1]}

def list_plusser(timedelta_list):
    # because sum() doesnt work for
    # non ints 
    sum_ret = datetime.timedelta()
    for x in timedelta_list:
        sum_ret += x
    return sum_ret

def stdev_finder(timedelta_list):
    # because stdev() doesnt work for
    # non ints 
    del_list = []
    for x in timedelta_list:
        del_list.append(x.total_seconds()) 
    return statistics.stdev(del_list)

def parse_results(host_count, filename, container_count):
    host_ct = int(host_count)
    fname = str(filename)
    conts = int(container_count)
    
    min_delay = datetime.timedelta.max
    max_delay = datetime.timedelta.min
    delay_cutoff = datetime.timedelta(minutes=1)
    delay_cutoff_min = datetime.timedelta()
    total_seqs = 0
    ave_delay = 0
    delay_list = []
    losses = []
    temp_delay_list = []
    temp_total_seqs = 0
    output_file = open('experiments/'+fname+'/results','w+')
    # go through container pairs
    for x in range(0,int(conts/2)):
        act_cont = str((x*2)+2)
        sen_cont = str((x*2)+1)
        for host_n in range(0,host_ct):
            if host_n % 2 == 0:
               try:
                     actuator_dir = 'experiments/'+fname+'/actuator/'+'52.74.73.'+act_cont+'/'
                     receiver_dir = 'experiments/'+fname+'/receiver/'+'13.55.147.'+sen_cont+'/'
                     actuator_file = open(actuator_dir+str(host_n)+'_actuator.log','r')
                     receiver_file = open(receiver_dir+str(host_n+1)+'_receiver.log','r')
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
                         try:
                            ac_time = datetime.datetime.strptime(ac_lines_parsed[seq],'%H:%M:%S.%f')
                            rc_time = datetime.datetime.strptime(rc_lines_parsed[seq],'%H:%M:%S.%f')
                            ms_delay = rc_time-ac_time
                            if (ms_delay <= delay_cutoff) and (ms_delay >= delay_cutoff_min):
                               delay_list.append(ms_delay)
                               temp_delay_list.append(ms_delay)
                               if ms_delay < min_delay:
                                   min_delay = ms_delay
                               if ms_delay > max_delay:
                                   max_delay = ms_delay
                            else:
                               overtime_count += 1
                         except:
                            pass

                     actual_responses = len(rc_lines_parsed) - overtime_count
                     total_seqs += actual_responses
                     temp_total_seqs += actual_responses
                     losses.append(int(len(ac_lines_parsed)) - int(len(rc_lines_parsed)) + overtime_count)
                     output_file.write(str(host_n)+","+str(host_n+1)+" pair : "+str(actual_responses)+"\n")
               except:
                     traceback.print_exc()
                     pass
               try:
                  output_file.write("ave delay : "+str(list_plusser(temp_delay_list)/temp_total_seqs)+"\n")
                  output_file.write("delay stdev : "+str(stdev_finder(temp_delay_list))+"\n")
               except:
                  output_file.write("average/stdev error\n")
               temp_delay_list = []
               temp_total_seqs = 0
    try:
        output_file.write("\n\n\n")
        output_file.write("mean losses : " + str(statistics.mean(losses)/200.0)+"\n")
        output_file.write("median losses : " + str(statistics.median(losses)/200.0)+"\n")
        output_file.write("mode losses : " + str(statistics.mode(losses)/200.0)+"\n")
    except:
        pass
    try:
        output_file.write("min delay : "+str(min_delay)+"\n")
        output_file.write("max delay : "+str(max_delay)+"\n")
        output_file.write("ave delay : "+str(list_plusser(delay_list)/total_seqs)+"\n")
        output_file.write("delay stdev : "+str(stdev_finder(delay_list))+"\n")
    except:
        pass

    output_file.close()

if __name__ == "__main__":
    parse_results(sys.argv[1], sys.argv[2], sys.argv[3])
