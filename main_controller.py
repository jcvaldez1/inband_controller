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
from ryu.lib.packet.ether_types import ETH_TYPE_IP
from ryu.lib.packet.in_proto import IPPROTO_TCP
import learning_switch
import requests, json
import ast, re
import socket, urllib2, uuid
from datetime import datetime
import time
from ryu.cfg import CONF
from constants import DOCKER_HOST_IPV4, IOT_ACCESS_POINT_IPV4, GATEWAY_IPV4, \
        DOCKER_HOST_ETH, IOT_ACCESS_POINT_ETH, GATEWAY_ETH, \
        FORWARDING_TABLE, REROUTING_TABLE

'''
        SDN_Rerouter is the main class that handles the rerouting flows
        part of the initialization would be to initialize a rerouting
        flow table as called via _init_reroute_table()
        @ATTRIBUTES
            datapaths       : key-value pairs of SDN switch datapath.ids to
                              the actual datapath value
            aliaser_thread  : thread running the aliaser function
'''
class SDN_Rerouter(learning_switch.BaseSwitch):

    def __init__(self, *args, **kwargs):
        #with open("./test.json" , "w") as outfile:
        #    json.dumps(CONF.__dict__, outfile, indent=4)
        #print(CONF.controller_mode)

        super(SDN_Rerouter, self).__init__(*args, **kwargs)
        self.datapaths = {}
        #self._init_reroute_table()
        self.aliaser_thread = hub.spawn(self._aliaser)


    '''
            initializes a dedicated flow table for the rerouting
            flows, and passes it to the forwarding table in the
            pipeline
    def _init_reroute_table(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionGotoTable(FORWARD_TABLE)]
        mod = parser.OFPFlowMod(datapath=datapath, table_id=FILTER_TABLE,
                                priority=1, instructions=inst)
        datapath.send_msg(mod)
        pass
    '''

    '''
            This function is responsible for the add_flow() function
            calls and is where all the rerouting flow configurations
            are generated
    '''
    def _aliaser(self):
        # datapath_id : (real, alias)
        while True:
            alias_test = self.aliases
            connection_health = self.live_connection("64.90.52.128")
            if (not connection_health):
                for alias_object in alias_test:
                    real_ip = alias_object['cloud_ip']
                    fake_ip = DOCKER_HOST_IPV4
                    real_port = alias_object['real_port']
                    fake_port = alias_object['fake_port']
                    for dp in self.datapaths.values():
                        ofproto = dp.ofproto
                        parser = dp.ofproto_parser
                        act_set = parser.OFPActionSetField
                        act_out = parser.OFPActionOutput
                        act_table = parser.OFPInstructionGotoTable
                        # OUTGOING 
                        actions = [ act_set(ipv4_dst=fake_ip),
                                    act_set(tcp_dst=fake_port),
                                    act_set(eth_dst=DOCKER_HOST_ETH) ]
                        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                        inst += [ act_table(FORWARDING_TABLE) ]
                        match = parser.OFPMatch( eth_type=ETH_TYPE_IP,
                                                 ip_proto=IPPROTO_TCP, # 6
                                                 ipv4_dst=real_ip,
                                                 tcp_dst=real_port)
                        super(SDN_Rerouter, self).add_flow(dp, REROUTE_FLOW_PRIORITY, match, inst)
                        # INCOMING  
                        actions = [ act_set(ipv4_src=real_ip),
                                    act_set(tcp_src=real_port),
                                    act_set(eth_src=GATEWAY_ETH) ]
                        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                        inst += [ act_table(FORWARDING_TABLE) ]
                        match = parser.OFPMatch( eth_type=ETH_TYPE_IP,
                                                 ip_proto=IPPROTO_TCP,
                                                 ipv4_src=fake_ip,
                                                 tcp_src=fake_port)
                        super(SDN_Rerouter, self).add_flow(dp, REROUTE_FLOW_PRIORITY, match, inst)
            hub.sleep(5)

    '''
            live_connection tests the connection health of a given hostname
            @PARAMS
                hostname    : the hostname of the host where its connection
                              with the controller is to be tested
            @RETURN
                bool_parse(stringer)    : boolean value whether the connection
                                          to hostname is deemed healthy or not
    '''
    def live_connection(self,hostname):

        '''
                bool_parse simply checks a string parameter
                and returns its boolean equivalent
        '''
        def bool_parse(string):
            if string == "True":
                return True
            elif string == "False":
                return False
            return

        url = hostname
        url = "64.90.52.128"
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

