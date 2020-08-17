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
    #included_groups = [1,2,5,10,20,25,50,100]
    #included_groups = [1,2,5,10,20,25]
    fname_mode = "device"
    #fname_mode = "container"
    subs = ["strong_nuc"]
    subs = ["weak_nuc"]
    cpu_data = init_list_dict(included_groups)
    mem_data = init_list_dict(included_groups)
    for submode in subs:
       for fname in included_groups:
           try:
                 file_name = "./"+fname_mode+"_variable/"+submode+"/"+str(fname)+"_pairs"
                 try:
                     file_ptr = open(file_name, "r")
                 except:
                     continue
                 file_data = file_ptr.readlines()
                 file_ptr.close()
  
                 cpu_flag = False
                 mem_flag = False
                 first_line = True
                 for line in file_data:
                     pruned_list = line.split(' ')
                     pruned_list = list(filter(('').__ne__, pruned_list))	
                     if len(pruned_list) < 5:
                        continue
                     if ("Average" in line) or (len(cpu_data[fname]) > 500):
                        break
                     if "idle" in line:
                        cpu_flag = True
                     elif cpu_flag:
                        cpu_flag = False
                        cpu_data[fname].append(100.0 - float(pruned_list[-1]))
                     if "memused" in line:
                        mem_flag = True
                     elif mem_flag:
                        mem_flag = False
                        mem_data[fname].append(float(pruned_list[5]))

                 x_axis = [ h for h in range(0,len(cpu_data[fname])) ]
                 y_axis = mem_data[fname]
                 y_axis = cpu_data[fname]
                 plt.plot(x_axis, y_axis, label = str(fname)+"_pairs") 

           except:
                 traceback.print_exc()
        # naming the x axis 
       plt.xlabel('Seconds') 
       # naming the y axis 
       plt.ylabel('cpu usage %') 
       plt.ylim(ymax=100)
       plt.ylim(ymin=0)
       plt.xlim(xmax=300)
       #plt.ylim(ymax=100)
       # giving a title to my graph 
       plt.title('Weak NUC cpu usage') 
         
       # show a legend on the plot 
       plt.legend() 
         
       # function to show the plot 
       plt.show() 

if __name__ == "__main__":
    #parse_results(sys.argv[1], sys.argv[2], sys.argv[3])
    parse_results()
