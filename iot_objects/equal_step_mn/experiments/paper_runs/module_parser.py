import datetime
import statistics
import sys
import traceback
import matplotlib.pyplot as plt

def parse_log_line(logline):
    buffer = logline.split()
    #return {'seq':buffer[3],'time':buffer[1]}
    # seq : time
    return buffer[1]

def list_plusser(timedelta_list):
    # because sum() doesnt work for
    # non ints 
    sum_ret = datetime.timedelta()
    for x in timedelta_list:
        sum_ret += x
    return sum_ret

def list_plusser_float(timedelta_list):
    # because sum() doesnt work for
    # non ints 
    sum_ret = 0.0
    for x in timedelta_list:
        sum_ret += x.total_seconds()
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
    throw = str(filename)
    conts = int(container_count)
    
    min_delay = datetime.timedelta.max
    max_delay = datetime.timedelta.min
    delay_cutoff = datetime.timedelta(minutes=1)
    delay_cutoff_min = datetime.timedelta()
    ave_delay = 0
    # go through container pairs
    included = [1,2,5,10,20,25,50,100]
    included = [1] + [ y for y in range(10,101,10) ]
    nuc_names = ["weak_nuc","strong_nuc"]
    mode_name = "container"
    mode_name = "device"
    for nuc_name in nuc_names:
       ave_del = []
       std_del = []
       for fname in included:
          delay_list = []
          total_seqs = 0
          for x in range(0,int(conts/2)):
              act_cont = str((x*2)+2)
              actuator_dir = mode_name+"_variable/"+nuc_name+"/"+str(fname)+'_pairs/actuator/'+'52.74.73.'+act_cont+'/'
              for host_n in range(0,fname,2):
                  try:
                        ac_lines_parsed = []
                        actuator_file = open(actuator_dir+str(host_n)+'_actuator.log','r')
                        ac_lines = actuator_file.readlines()
                        actuator_file.close()
                        for line in ac_lines:
                            ac_lines_parsed.append(parse_log_line(line))
              
                        first_stamp = True
                        prev_stamp = None
                        for timestamp in ac_lines_parsed:
                            try:
                               ac_time = datetime.datetime.strptime(timestamp,'%H:%M:%S.%f')
                               if first_stamp:
                                  first_stamp = False
                                  prev_stamp = ac_time
                               else:
                                  ms_delay = ac_time-prev_stamp
                                  prev_stamp = ac_time
                                  delay_list.append(ms_delay)
                            except:
                               pass

                        total_seqs += len(ac_lines_parsed)
                  except:
                        traceback.print_exc()
                        pass
          pass
          ave_del.append(list_plusser_float(delay_list)/total_seqs)
          std_del.append(stdev_finder(delay_list))
       x_axis = included
       if nuc_name == "weak_nuc":
          x_axis = included[:-2]
       color_1 = "#15acee"
       color_2 = "#a3def8"
       if nuc_name == "strong_nuc":
          color_1 = "#f9717f"
          color_2 = "#ffaa94"
       plt.plot(x_axis, ave_del, color = color_1, label = nuc_name, linewidth = 5)
       plt.plot(x_axis, std_del, color = color_2,label = nuc_name+" std dev", linewidth = 5)
    plt.xlabel('Container Pairs')
    # naming the y axis 
    plt.ylabel('Seconds per Request')
    plt.ylim(ymin=0)
    # giving a title to my graph 
    plt.title('Actual Request Frequency (100 device pairs)')

    # show a legend on the plot 
    plt.legend()

    # function to show the plot 
    plt.show()


if __name__ == "__main__":
    parse_results(sys.argv[1], sys.argv[2], sys.argv[3])
