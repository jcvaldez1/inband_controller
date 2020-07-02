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
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, \
        CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.packet.ether_types import ETH_TYPE_IP
from ryu.lib.packet.in_proto import IPPROTO_TCP
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
import learning_switch
import requests, json
import ast, re
import socket, uuid
from datetime import datetime
import time
from ryu.cfg import CONF
from constants import DOCKER_HOST_IPV4, IOT_ACCESS_POINT_IPV4, GATEWAY_IPV4, \
        DOCKER_HOST_ETH, IOT_ACCESS_POINT_ETH, GATEWAY_ETH, CONTROLLER_ETH,\
        FORWARDING_TABLE, REROUTING_TABLE, REGISTRATION_IP, \
        DEFAULT_PORT_COUNTER, REROUTE_FLOW_PRIORITY, REROUTE_FLOW_PRIORITY_DUAL_ROLE,\
        DEFAULT_CONFIG_PORT
from alias_object import Alias
import traceback
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
        self.aliases   = []
        self.registered_users = []
        self.registered_clouds = []
        self.port_counter = DEFAULT_PORT_COUNTER
        self.aliaser_thread = hub.spawn(self._aliaser)
        # TEST ENTRIES FIRST
        #cloud_ip = "52.74.73.81"
        #cloud_ip2 = "13.55.147.2"
        #kwargs = {"real_port":80, "fake_port":42069, "cloud_ip":cloud_ip}
        #self.aliases.append(Alias(**kwargs))
        #kwargs = {"real_port":80, "fake_port":5000, "cloud_ip":cloud_ip2}
        #self.aliases.append(Alias(**kwargs))
        #kwargs = {"real_port":42915, "fake_port":42917, "cloud_ip":cloud_ip}
        #self.aliases.append(Alias(**kwargs))
        #kwargs = {"real_port":42915, "fake_port":42915, "cloud_ip":cloud_ip2}
        #self.aliases.append(Alias(**kwargs))


    '''
            initializes a dedicated flow table for the rerouting
            flows, and passes it to the forwarding table in the
            pipeline
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _init_reroute_table(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # register flow
        match = parser.OFPMatch(eth_type=ETH_TYPE_IP,
                                ipv4_dst=REGISTRATION_IP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        actions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        self.add_flow(datapath, REROUTING_TABLE, 25, match, actions, None, True)

    '''
            This function triggers on PACKET_IN event
            it currently contains the following functionalities
            related to the rerouting section of the pipeline:
                -   IoT device registration
    '''
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_reroute(self, ev):
        try:
            msg = ev.msg
            pkt = packet.Packet(msg.data)
            ip = pkt.get_protocol(ipv4.ipv4)
            if ip:
                if ip.dst == REGISTRATION_IP:
                    self.register_device(pkt.protocols[-1])
        except:
            self.logger.debug("failed to register device %s", json_string)
            raise
        return

    '''
            This function is responsible for the add_flow() function
            calls and is where all the rerouting flow configurations
            are generated
    '''
    def _aliaser(self):
        # datapath_id : (real, alias)
        while True:
            #connection_health = self.live_connection("64.90.52.128")
            alias_test = self.aliases
            print("\nalias_list : "+str(self.aliases)+"\n")
            #alias_test = []
            #if (not connection_health):
            #    alias_test = self.aliases
            #else:
            #    cloud_ip = "52.74.73.81"
            #    kwargs = {"real_port":80, "fake_port":42069, "cloud_ip":cloud_ip}
            #    alias_test.append(Alias(**kwargs))
            #    kwargs = {"real_port":42915, "fake_port":42917, "cloud_ip":cloud_ip}
            #    alias_test.append(Alias(**kwargs))
            connection_health = False
            if (not connection_health):
                print("\n\nADDING FLOWS\n\n")
                for alias_ob in alias_test:
                    real_ip = alias_ob.cloud_ip
                    fake_ip = DOCKER_HOST_IPV4
                    real_port = alias_ob.real_port
                    fake_port = alias_ob.fake_port
                    for dp in self.datapaths.values():
                        ofproto = dp.ofproto
                        parser = dp.ofproto_parser
                        act_set = parser.OFPActionSetField
                        act_out = parser.OFPActionOutput
                        act_table = parser.OFPInstructionGotoTable

                        # NORMAL REROUTE FLOW SET
                        # OUTGOING 
                        actions = [ act_set(ipv4_dst=fake_ip),
                                    act_set(tcp_dst=fake_port),
                                    act_set(eth_dst=DOCKER_HOST_ETH) ]
                        #actions += [ act_out(5) ]
                        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                        inst += [ act_table(FORWARDING_TABLE) ]
                        match = parser.OFPMatch( eth_type=ETH_TYPE_IP,
                                                 ip_proto=IPPROTO_TCP, # 6
                                                 ipv4_src=IOT_ACCESS_POINT_IPV4,
                                                 ipv4_dst=real_ip,
                                                 tcp_dst=real_port)
                        super(SDN_Rerouter, self).add_flow(dp, REROUTING_TABLE, REROUTE_FLOW_PRIORITY, match, inst)
                        # INCOMING  
                        actions = [ act_set(ipv4_src=real_ip),
                                    act_set(tcp_src=real_port),
                                    act_set(eth_src=GATEWAY_ETH) ]
                        #actions += [ act_out(3) ]
                        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                        inst += [ act_table(FORWARDING_TABLE) ]
                        match = parser.OFPMatch( eth_type=ETH_TYPE_IP,
                                                 ip_proto=IPPROTO_TCP,
                                                 ipv4_dst=IOT_ACCESS_POINT_IPV4,
                                                 ipv4_src=fake_ip,
                                                 tcp_src=fake_port)
                        super(SDN_Rerouter, self).add_flow(dp, REROUTING_TABLE, REROUTE_FLOW_PRIORITY, match, inst)


                        # FOR CASES WHERE CLIENT == ALIAS
                        # OUTGOING 
                        actions = [ 
                                    act_set(ipv4_dst=fake_ip),
                                    act_set(tcp_dst=fake_port),
                                    act_set(eth_dst=DOCKER_HOST_ETH),
                                    act_set(ipv4_src=real_ip),
                                    act_set(eth_src=GATEWAY_ETH),
                                    ]
                        #actions += [ act_out(5) ]
                        actions += [ act_out(ofproto.OFPP_IN_PORT) ]
                        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                        #inst += [ act_table(FORWARDING_TABLE) ]
                        match = parser.OFPMatch( eth_type=ETH_TYPE_IP,
                                                 ip_proto=IPPROTO_TCP, # 6
                                                 ipv4_src=fake_ip,
                                                 ipv4_dst=real_ip,
                                                 tcp_dst=real_port)
                        super(SDN_Rerouter, self).add_flow(dp, REROUTING_TABLE, REROUTE_FLOW_PRIORITY_DUAL_ROLE, match, inst)
                        # INCOMING  
                        actions = [ act_set(ipv4_src=real_ip),
                                    act_set(tcp_src=real_port),
                                    act_set(eth_src=GATEWAY_ETH),
                                    act_set(ipv4_dst=fake_ip),
                                    act_set(eth_dst=DOCKER_HOST_ETH),
                                    ]
                        #actions += [ act_out(5) ]
                        actions += [ act_out(ofproto.OFPP_IN_PORT) ]
                        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
                        #inst += [ act_table(FORWARDING_TABLE) ]
                        match = parser.OFPMatch( eth_type=ETH_TYPE_IP,
                                                 ip_proto=IPPROTO_TCP,
                                                 ipv4_src=fake_ip,
                                                 ipv4_dst=real_ip,
                                                 tcp_src=fake_port)
                        super(SDN_Rerouter, self).add_flow(dp, REROUTING_TABLE, REROUTE_FLOW_PRIORITY_DUAL_ROLE, match, inst)

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
        url = "https://whois.org/"
        command = "python3 ./connection_tester.py "+url
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,shell=True)
        stringer = proc.communicate()[0][:-1]
        exit_code = proc.wait()
        stringer = stringer.decode("utf8")
        print("\n\n\n" + str(stringer) +"\n\n\n")
        return bool_parse(str(stringer))

    '''
            registers a new device by creating an Alias() object
            and storing it in the self.aliases alias list for
            tracking the registered cloud services

            @PARAMS:
                json_string     : payload data that came from the registration
                                  packet sent by an IoT device. This should 
                                  contain the following information:
                                    - ['ports']     = port numbers that the IoT
                                                      device plans to use
                                    - ['cloud_ip']  = the IPv4 address of the
                                                      cloud service the IoT device
                                                      plans to use
                                    - ['users']     = list of users that this
                                                      device is registered to
                                    - ['device_id'] = can be sent by device or
                                                      any be any randomly
                                                      generated hash string
    '''
    def register_device(self, json_string):
        port_rollback = self.port_counter
        try:
            #port_rollback = self.port_counter
            new_obj = json.loads(json_string)
            new_alias = None
            print("\n"+str(new_obj)+"\n")
            if ( "ports" in new_obj ) and ( "cloud_ip" in new_obj ) and (new_obj["cloud_ip"] not in self.registered_clouds):
                self.registered_clouds.append(new_obj['cloud_ip'])
                for port in new_obj['ports']:
                    new_alias = Alias(real_port=port, fake_port=self.port_counter, cloud_ip=new_obj['cloud_ip'], name=new_obj['name'])
                    self.port_counter += 1
                #new_alias['cloud_ip'] = new_obj['cloud_ip']
                    self.aliases.append(new_alias)
                self.register_new_user([new_obj['user_id']])
            else:
                try:
                    self.register_new_user(new_obj['users'])
                except:
                    traceback.print_exc()
        except:
            self.port_counter = port_rollback
            traceback.print_exc()
            try:
                self.logger.debug("failed to register device %s", json_string)
            except:
                self.logger.info("json string is not in JSON string format")
            raise
                #traceback.print_exc()

    '''
            Registers user
    '''
    def register_new_user(self, user_id_list):
        for user_id in user_id_list:
            if user_id not in self.registered_users:
                self.registered_users.append(user_id)
        return

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

