#import subprocess
#url = "www.8ch.net"
#while True:
#    #exit_code = subprocess.call("python /home/thesis/net_elements/controller_code/connection_tester.py " + url, shell=True)
#
#
#    proc = subprocess.Popen(['python','/home/thesis/net_elements/controller_code/connection_tester.py',  url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#    print(proc.communicate()[0][:-1])
#    exit_code = proc.wait()
#    #print(exit_code)
#    #a = subprocess.call('python /home/thesis/net_elements/controller_code/connection_tester.py ' +url)

import subprocess
import sys
def live_connection(hostname):

    def bool_parse(string):
        if string == "True":
            return True
        elif string == "False":
            return False
    #print("\n\n\nSTARTING POLLER\n\n\n")
    url = hostname
    command = "python ./connection_tester.py "+url
    print(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,shell=True)
    stringer = proc.communicate()[0][:-1]
    exit_code = proc.wait()
    print("\n\n\nENDING POLLER"+ str(stringer)+ "\n\n\n")
    return bool_parse(stringer)

if __name__ == "__main__":
    live_connection(sys.argv[1])
