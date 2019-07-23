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

from operator import attrgetter 
#from ryu.app import meter_poller
#import meter_poller
import learning_switch
import os
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub


# IMPORT NEVESSARY LIBRARIES FOR THE NFVs
import socket
import requests
import constants
import json
from datetime import datetime
import aliaser
import os
from subprocess import call
import ast
import urllib2
from ryu.cfg import CONF
import sys
import subprocess
import time
import testboi
sys.path.insert(0, '/home/thesis/net_elements/devstack_api')


class SimpleMonitor13(testboi.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        #with open("./test.json" , "w") as outfile:
        #    json.dumps(CONF.__dict__, outfile, indent=4)
        #print(CONF.controller_mode)

        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}

        # TEMPORARY CONSTANTS
        self.SELF_IP = "192.168.85.251"
        self.INTERNET_PORT = 5
        self.CLIENT_SWITCH_PORT = 4
        self.HOSTNAME_IPS = {}
        self.IP_STATUS = {}
        self.aliaser_thread = hub.spawn(self._aliaser_boi)
        #hub.spawn(self._monitor)

    def _aliaser_boi(self):
        hub.sleep(20)
        # datapath_id : (real, alias)
        #alias_test = {1:("10.0.0.2","10.0.0.3"),2:("10.0.0.3","10.0.0.4")}
        alias_test = { 1:("8.8.8.8","10.147.4.56") }
        #alias_test = { 1:("192.168.1.194","192.168.1.222") }
        up_flag = True
        while True:
            print("\n\n\n"+str(self.mac_to_port)+"\n\n\n\n")
            for key, val in alias_test.iteritems():
                #print("\n\n\n" + str(key) + str(val))
                #real_ip=self._validate_ip(val[0])
                #fake_ip=self._validate_ip(val[1])
                real_ip = val[0]
                fake_ip = val[1]
                connection_health = self.live_connection(real_ip)
                #connection_health = False

                if (not connection_health) and (up_flag):
                    up_flag = not up_flag
                    for dp in self.datapaths.values():
                        if dp.id != 1:
                            ofproto = dp.ofproto
                            parser = dp.ofproto_parser
                            act_set = parser.OFPActionSetField
                            act_out = parser.OFPActionOutput
                            # REWRITE ARP REQS AND REPS FIRST
                            #receiver_mac_add = "f4:f2:6d:d6:88:2f"
                            #sender_mac_add = "f4:f2:6d:c7:37:ef"
                            #sender_mac_add = "34:f6:4b:92:20:bb"
                            #sender_mac_add = "f4:f2:6d:c7:5f:d1"
                            #switch_mac_add = "70:b3:d5:6c:da:15"
                            #receiver_mac_add = "98:ee:cb:45:b9:08"
                            #sender_mac_add = "98:ee:cb:45:b8:e6"
                            #switch_mac_add = "44:d1:fa:62:96:06"
                            switch_mac_add = "9c:dc:71:f0:c7:c0"
                            sender_mac_add = "a8:40:41:1b:21:52"
                            #switch_mac_add = "70:b3:d5:6c:da:15"
                            receiver_mac_add = "98:ee:cb:45:b9:08"
                            #match = parser.OFPMatch(eth_type=0x0806, arp_op=1,
                            #                       arp_sha=sender_mac_add,arp_tpa="192.168.1.1")
                            #actions = [act_set(arp_tpa=fake_ip),
                            #           act_set(eth_dst=receiver_mac_add),
                            #           act_out(self.mac_to_port[dp.id][receiver_mac_add]) ]
                            #super(SimpleMonitor13, self).add_flow(dp, 15, match, actions)
                            # REP HANDLER
                            #match = parser.OFPMatch(eth_type=0x0806, arp_op=2,
                            #                       arp_sha=receiver_mac_add,arp_tpa="192.168.1.223")
                            #actions = [act_set(arp_sha=switch_mac_add),
                            #           act_set(eth_dst=receiver_mac_add),
                            #           act_out(self.mac_to_port[dp.id][sender_mac_add]) ]
                            #super(SimpleMonitor13, self).add_flow(dp, 15, match, actions)

                           # dp = self.datapaths[key]
                            # OUTGOING 
                            #mac_add = self.ip_to_mac[dp.id][val[1]]
                            actions = [ act_set(ipv4_dst=fake_ip),
                                       act_set(eth_dst=receiver_mac_add),
                                       #act_set(eth_dst=mac_add),
                                       act_out(self.mac_to_port[dp.id][receiver_mac_add]) ]
                            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=real_ip)
                            super(SimpleMonitor13, self).add_flow(dp, 15, match, actions)

                            # INGOING
                            #mac_add = self.ip_to_mac[dp.id]["192.168.1.242"]
                            actions = [
                                act_set(ipv4_src=real_ip),
                                act_set(eth_src=switch_mac_add),
                                act_out(self.mac_to_port[dp.id][sender_mac_add]) ]
                            match = parser.OFPMatch(eth_type=0x0800, ipv4_src=fake_ip)
                            super(SimpleMonitor13, self).add_flow(dp, 15, match, actions)
                else:
                    # REMOVE SHITTY FLOWS
                    pass

                    #print("\n\n\nEXEMPT CONTROLLER\n\n\n")
                    #actions = [ parser.OFPActionOutput(constants.INTERNET_SWITCH_PORT) ]
                    #match = parser.OFPMatch(eth_type=0x0800,ipv4_dst=real_ip,eth_src=constants.CONTROLLER_ETH)
                    #super(SimpleMonitor13, self).add_flow(dp, 15, match, actions, None,True)

                    #actions = [ parser.OFPActionOutput(constants.CONTROLLER_SWITCH_PORT) ]
                    #match = parser.OFPMatch(eth_type=0x0800,ipv4_src=real_ip,eth_dst=constants.CONTROLLER_ETH)
                    #super(SimpleMonitor13, self).add_flow(dp, 15, match, actions, None,True)

            hub.sleep(5)

    def live_connection(self,hostname):

        def bool_parse(string):
            if string == "True":
                return True
            elif string == "False":
                return False
        #print("\n\n\nSTARTING POLLER\n\n\n")
        url = hostname
        #if hostname == "8.8.8.8":
        url = "127.0.0.1:8000"
        command = "python ./connection_tester.py "+url
        print(command+"\n\n\n")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,shell=True)
        stringer = proc.communicate()[0][:-1]
        exit_code = proc.wait()
        print("\n\n\nENDING POLLER "+ str(stringer)+ "\n\n\n")
        return bool_parse(stringer)

    def _validate_ip(self, ip_add, status=True):

        def bool_parse(string):
            if (string == "False") or (string == "None"):
                return False
            else:
                return string
        #print("\n\n\nSTARTING VALIDATOR\n\n\n")
        url = ip_add

        proc = subprocess.Popen(['python','/home/thesis/net_elements/controller_code/ip_validator.py',  url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stringer = proc.communicate()[0][:-1]
        exit_code = proc.wait()
        #print("\n\n\nENDING VALIDATOR"+ str(stringer)+ "\n\n\n")
        the_val = bool_parse(stringer)
        if not the_val:
            try:
                the_val = self.IP_STATUS[ip_add]
            except:
                print("NO IP AVAILABLE FOR "+ip_add)
                sys.exit(1)

        self.IP_STATUS[ip_add] = the_val
        return the_val

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

    def _monitor(self):
        while True:
            self.currently_banned_ips = []
            print(str(self.datapaths)+"\n\n\n")
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(8)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info('datapath         '
                         'in-port  eth-dst           '
                         'out-port packets  bytes')
        self.logger.info('---------------- '
                         '-------- ----------------- '
                         '-------- -------- --------')
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.info(stat)
            self.logger.info('%016x %8x %17s %8x %8d %8d',
                             ev.msg.datapath.id,
                             stat.match['in_port'], stat.match['eth_dst'],
                             stat.instructions[0].actions[0].port,
                             stat.packet_count, stat.byte_count)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
                             ev.msg.datapath.id, stat.port_no,
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors)
