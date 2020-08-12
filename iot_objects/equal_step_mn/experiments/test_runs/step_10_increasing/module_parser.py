import datetime
import statistics
import sys
import traceback
import matplotlib.pyplot as plt 

def parse_log_line(logline):
    buffer = logline.split()
    #return {'seq':buffer[3],'time':buffer[1]}
    # seq : time
    return {buffer[3]:buffer[1]}

def get_seq_num(logline):
    buffer = logline.split()
    #return {'seq':buffer[3],'time':buffer[1]}
    # seq : time
    return int(buffer[3])

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

def parse_results(host_count=0, filename="", container_count=0):
    #host_ct = int(host_count)
    #fname = str(filename)
    #conts = int(container_count)
    
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
    # go through container pairs
    x_axis = [ x for x in range(0,200)]
    included_groups = [0,10,20]
    included_groups = [50,80,100]
    #for fname in range(0,101,10):
    for fname in included_groups:
        try:
              actuator_dir = str(fname)+'_dev_pair_inc/actuator/52.74.73.2/'
              receiver_dir = str(fname)+'_dev_pair_inc/receiver/13.55.147.1/'
              actuator_file = open(actuator_dir+'0_actuator.log','r')
              receiver_file = open(receiver_dir+'1_receiver.log','r')
              ac_lines = actuator_file.readlines()
              rc_lines = receiver_file.readlines()
              ac_lines_parsed = {}
              rc_lines_parsed = {}
              actuator_file.close()
              receiver_file.close()
              overtime_count = 0
              first_line = True
              request_offset = 0
              for line in ac_lines:
                  ac_lines_parsed = {**ac_lines_parsed, **parse_log_line(line)}
                  if first_line:
                     request_offset = get_seq_num(line)
                     first_line = False
                  
              for line in rc_lines:
                  rc_lines_parsed = {**rc_lines_parsed, **parse_log_line(line)}

              default_time_deltas = [datetime.timedelta(minutes=1)] * 200
              for seq in rc_lines_parsed:
                  try:
                     ac_time = datetime.datetime.strptime(ac_lines_parsed[seq],'%H:%M:%S.%f')
                     rc_time = datetime.datetime.strptime(rc_lines_parsed[seq],'%H:%M:%S.%f')
                     ms_delay = rc_time-ac_time
                     if ms_delay > delay_cutoff:
                        ms_delay = delay_cutoff
                     default_time_deltas[int(seq)-request_offset] = ms_delay
                  except:
                     traceback.print_exc()
                     pass
              y_axis = [ y.total_seconds() for y in default_time_deltas ]
              plt.plot(x_axis, y_axis, label = "pairs "+str(fname)) 

        except:
              traceback.print_exc()
        # naming the x axis 
    plt.xlabel('Requests') 
    # naming the y axis 
    plt.ylabel('Seconds Delay') 
    # giving a title to my graph 
    plt.title('Delay for each request on the First device pair') 
      
    # show a legend on the plot 
    plt.legend() 
      
    # function to show the plot 
    plt.show() 

if __name__ == "__main__":
    #parse_results(sys.argv[1], sys.argv[2], sys.argv[3])
    parse_results()
