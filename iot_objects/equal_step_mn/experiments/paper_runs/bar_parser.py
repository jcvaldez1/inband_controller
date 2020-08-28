import datetime
import statistics
import sys
import traceback
import matplotlib.pyplot as plt 
import matplotlib.axes
import numpy as np

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

def init_list_dict(groups):
    ret_dict = {}
    for x in groups:
        ret_dict[x] = []
    return ret_dict

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
    included_groups = [1] + [ y for y in range(10,101,10) ]
    included_groups = [1,2,5,10,20,25,50,100]
    included_groups = input("enter pair numbers in ascending order separated by comma (e.g. 1,5,15,30,...) : ").split(",")
    included_groups = [int(x) for x in included_groups]
    fname_mode = "device"
    fname_mode = "container"
    fname_mode = input("Read data files from device or container mode subdirectory? : ")
    submode = ["weak_nuc","strong_nuc"]
    cpu_data = init_list_dict(included_groups)
    mem_data = init_list_dict(included_groups)
    x_axis = included_groups
    y_data = {}
    for sub in submode:
        for fname in included_groups:
            try:
                  file_name = "./"+fname_mode+"_variable/"+sub+"/"+str(fname)+"_pairs/results"
                  #print(fname)
                  try:
                      file_ptr = open(file_name, "r")
                  except:
                      #print("HERE")
                      y_data.setdefault(sub+"_loss", []).append(100)
                      y_data.setdefault(sub+"_ave_del", []).append(25000)
                      y_data.setdefault(sub+"_std_del", []).append(25000)
                      continue
                  file_data = file_ptr.readlines()
                  file_ptr.close()
  
                  cpu_flag = False
                  mem_flag = False
                  first_line = True
                  for line in reversed(file_data):
                      pruned_list = line.split(' : ')
                      pruned_list = list(filter(('').__ne__, pruned_list))	
                      #if len(pruned_list) < 5:
                      #   continue
                      if ("mean losses" in line):
                         y_data.setdefault(sub+"_loss", []).append(float(pruned_list[-1]))
                         break
                      if 'ave delay' in pruned_list:
                         del_data = pruned_list[-1].split(":")[-1]
                         y_data.setdefault(sub+"_ave_del", []).append(1000.0 * float(del_data))
                      if 'delay stdev' in pruned_list:
                         y_data.setdefault(sub+"_std_del", []).append(1000.0 * float(pruned_list[-1]))
            except:
                  traceback.print_exc()
            # naming the x axis 
    print(y_data)
    labels = included_groups
    
    x = np.arange(len(labels))  # the label locations
    width = 0.30  # the width of the bars
    
    fig, ax = plt.subplots()
    #men_means = [20, 34, 30, 35, 27]
    #women_means = [25, 32, 34, 20, 25]
    #rects1 = ax.bar(x - width/2, men_means , width, label='Men')
    #rects2 = ax.bar(x + width/2, women_means, width, label='Women')
    #y_axis = y_data["weak_nuc_ave_del"]
    #ax.bar(x - 0.30, y_axis, color = '#15acee', width = width, label = "weak_nuc_average_delay")
    #y_axis = y_data["weak_nuc_std_del"]
    #ax.bar(x - 0.10, y_axis, color = '#a3def8', width = width, label = "weak_nuc_stdev")
    #y_axis = y_data["strong_nuc_ave_del"]
    #ax.bar(x + 0.10, y_axis, color = '#f9717f', width = width, label = "strong_nuc_average_delay")
    #y_axis = y_data["strong_nuc_std_del"]
    #ax.bar(x + 0.30, y_axis, color = '#ffaa94', width = width, label = "strong_nuc_stdev")
    y_axis = y_data["weak_nuc_loss"]
    ax.bar(x - 0.15, y_axis, color = '#15acee', width = width, label = "weak_nuc")
    y_axis = y_data["strong_nuc_loss"]
    ax.bar(x + 0.15, y_axis, color = '#f9717f', width = width, label = "strong_nuc")
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    #ax.set_ylabel('Milliseconds')
    ax.set_ylabel('Percent loss')
    ax.set_xlabel('Container pairs')
    ax.set_title('Losses')
    ax.set_xticks(x)
    plt.ylim(ymax=1)
    plt.ylim(ymin=0)
    ax.set_xticklabels(labels)
    ax.legend()
    
    
    
    fig.tight_layout()

    #for x in submode:
        #y_axis = y_data[x+"_ave_del"]
        #plt.plot(x_axis, y_axis, label = x+"_average_delay") 
        #y_axis = y_data[x+"_std_del"]
        #plt.plot(x_axis, y_axis, label = x+"_stdev") 
        #y_axis = y_data[x+"_loss"]
        #plt.plot(x_axis, y_axis, label = x+"_losses") 




    #plt.xlabel('Device Pairs') 
    ## naming the y axis 
    #plt.ylabel('Milliseconds') 
    ##plt.ylim(ymin=0)
    ##plt.ylim(ymax=1)
    ## giving a title to my graph 
    #plt.title('Delay and Stdev') 
    #  
    ## show a legend on the plot 
    #plt.legend() 
    #  
    ## function to show the plot 
    plt.show() 

if __name__ == "__main__":
    #parse_results(sys.argv[1], sys.argv[2], sys.argv[3])
    parse_results()
