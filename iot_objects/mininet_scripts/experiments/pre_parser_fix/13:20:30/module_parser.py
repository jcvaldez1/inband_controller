import datetime
import statistics
import sys

def parse_log_line(logline):
    buffer = logline.split()
    #return {'seq':buffer[3],'time':buffer[1]}
    # seq : time
    return {buffer[3]:buffer[1]}

def parse_results(host_count, filename):
    host_ct = int(host_count)
    fname = str(filename)
    
    min_delay = 10000
    max_delay = 0
    total_seqs = 0
    ave_delay = 0
    delay_list = []
    losses = []
    #output_file = open('experiments/'+fname+'/results','w+')
    
    #for host_n in range(2,host_ct):
    for host_n in range(2,5):
        if host_n % 2 == 0:
           try:
                 host_pair_buffer = []
                 host_pair_buffer.append('---actuator '+str(host_n)+' and '+'receiver '+str(host_n+1)+'---\n')
                 actuator_file = open('./actuator/'+str(host_n)+'_actuator_log.log','r')
                 receiver_file = open('./receiver/'+str(host_n+1)+'_receiver_log.log','r')
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
                     #print(str(ac_time), str(rc_time))
                     #ms_delay = (rc_time-ac_time).microseconds
                     #print(str(ms_delay))
                     ms_delay = (rc_time-ac_time).microseconds/1000
                     delay_list.append(ms_delay)
                     if ms_delay < min_delay:
                         min_delay = ms_delay
                     if ms_delay > max_delay:
                         max_delay = ms_delay
                     #print(ms_delay)
                     #host_pair_buffer.append(str(ms_delay)+'\n')
                 total_seqs += len(rc_lines_parsed)
                 losses.append( int(len(ac_lines_parsed))- int(len(rc_lines_parsed)))
                 #output_file.write(str(host_n)+","+str(host_n+1)+" pair : "+str(len(rc_lines_parsed))+"\n")
                 #output_file.writelines(host_pair_buffer)
           except:
                 pass
    #try:
    #    output_file.write("mean losses : " + str(statistics.mean(losses))+"\n")
    #    output_file.write("median losses : " + str(statistics.median(losses))+"\n")
    #    output_file.write("mode losses : " + str(statistics.mode(losses))+"\n")
    #except:
    #    pass
    #output_file.write("min : "+str(min_delay)+"\n")
    #output_file.write("max : "+str(max_delay)+"\n")
    #output_file.write("ave : "+str(sum(delay_list)/total_seqs)+"\n")
    #output_file.close()

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
