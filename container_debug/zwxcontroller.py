# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# BASE RYU PACKAGE REQS
from operator import attrgetter 
import os
import sys
import subprocess
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import learning_switch
import requests, json
import ast, re
import socket, urllib2, uuid
from datetime import datetime
import time
from ryu.cfg import CONF


class SDN_Rerouter(learning_switch.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        #with open("./test.json" , "w") as outfile:
        #    json.dumps(CONF.__dict__, outfile, indent=4)
        #print(CONF.controller_mode)

        super(SDN_Rerouter, self).__init__(*args, **kwargs)
        self.datapaths = {}

        # TEMPORARY CONSTANTS
        self.aliaser_thread = hub.spawn(self._aliaser_boi)

    def _aliaser_boi(self):
        #hub.sleep(20)
        # datapath_id : (real, alias)
        recv_ip = "192.168.85.254"
        while True:
            alias_test = self.aliases
            print("\n\n\n"+str(self.mac_to_port)+"\n"+str(self.ip_to_mac)+"\n\n\n\n")
            connection_health = self.live_connection("asdf")
            if (not connection_health):
                for val in alias_test.values():
                    port_val = val[0]
                    ip_val = val[1]
                    real_ip = ip_val[0]
                    fake_ip = ip_val[1]
                    real_port = port_val[0]
                    fake_port = port_val[1]
                    for dp in self.datapaths.values():
						ofproto = dp.ofproto
						parser = dp.ofproto_parser
						act_set = parser.OFPActionSetField
						act_out = parser.OFPActionOutput
						# DHserver mac
						switch_mac_add = "9c:dc:71:f0:c7:c0"
						switch_mac_add = "6c:3b:6b:9d:c7:c7"
                        #switch_mac_add = "a8:60:b6:10:c6:4d"
						# Wifi gateway mac
						sender_mac_add = "a8:40:41:1b:21:52"
						#sender_mac_add = "50:3e:aa:04:e6:39"
						# self mac
						receiver_mac_add = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
						#receiver_mac_add = "a8:60:b6:11:e2:b7"
						#receiver_mac_add = "50:3e:aa:59:60:e7"
						#receiver_mac_add = "a8:60:b6:10:be:a1"

						# OUTGOING 
						actions = [ act_set(ipv4_dst=fake_ip),
								#	act_set(ipv4_src=real_ip),
									act_set(tcp_dst=fake_port),
									act_set(eth_dst=receiver_mac_add),
								    act_out(1) ]
						match = parser.OFPMatch(eth_type=0x0800,
												ipv4_dst=real_ip,
												ip_proto=6, #TCP,
												ipv4_src=recv_ip,
                              tcp_dst=real_port)
						super(SDN_Rerouter, self).add_flow(dp, 15, match, actions)

						# INCOMING  
						actions = [
							act_set(ipv4_src=real_ip),
							#act_set(ipv4_dst=recv_ip),
							act_set(tcp_src=real_port),
							act_set(eth_src=switch_mac_add),
							#act_set(eth_dst=sender_mac_add),
							act_out(2) ]
						match = parser.OFPMatch(eth_type=0x0800,
												ipv4_src=fake_ip,
												ip_proto=6, #TCP,
												#ipv4_dst=real_ip,
												ipv4_dst=recv_ip,
                              tcp_src=fake_port)
						super(SDN_Rerouter, self).add_flow(dp, 25, match, actions)
            hub.sleep(5)

    def live_connection(self,hostname):

        def bool_parse(string):
            if string == "True":
                return True
            elif string == "False":
                return False

        url = hostname
        url = "64.90.52.128"
        #url = "127.0.0.1:8000"
        command = "python ./connection_tester.py "+url
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,shell=True)
        stringer = proc.communicate()[0][:-1]
        exit_code = proc.wait()
        return bool_parse(stringer)


    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

