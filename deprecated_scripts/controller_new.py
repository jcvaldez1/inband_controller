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
import packet_in_test
import re, uuid


class SimpleMonitor13(packet_in_test.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        #with open("./test.json" , "w") as outfile:
        #    json.dumps(CONF.__dict__, outfile, indent=4)
        #print(CONF.controller_mode)

        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}

        self.alias_ip = "192.168.85.253"
        self.recv_ip = "192.168.85.252"
        self.alias_test = { 1:((80,4000),("64.90.52.128",self.alias_ip)), 2:((80,5000),("52.230.1.186",self.alias_ip))}

        self.aliaser_thread = hub.spawn(self._aliaser_boi)
        #hub.spawn(self._monitor)

    def _aliaser_boi(self):
        hub.sleep(20)
        # datapath_id : (real, alias)
        while True:
            print("\n\n\n"+str(self.mac_to_port)+"\n"+str(self.ip_to_mac)+"\n\n\n\n")
            for key, val in self.alias_test.iteritems():
                #print("\n\n\n" + str(key) + str(val))
                #real_ip=self._validate_ip(val[0])
                #fake_ip=self._validate_ip(val[1])
                port_val = val[0]
                ip_val = val[1]
                real_ip = ip_val[0]
                fake_ip = ip_val[1]
                real_port = port_val[0]
                fake_port = port_val[1]
                connection_health = self.live_connection(real_ip)
                if (not connection_health):
                    for dp in self.datapaths.values():
                        ofproto = dp.ofproto
                        parser = dp.ofproto_parser
                        act_set = parser.OFPActionSetField
                        act_out = parser.OFPActionOutput
                        # DHserver mac
                        switch_mac_add = "9c:dc:71:f0:c7:c0"
                        switch_mac_add = "6c:3b:6b:9d:c7:c7"
                        # Wifi gateway mac
                        sender_mac_add = "a8:40:41:1b:21:52"
                        # self mac
                        receiver_mac_add = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
                        #receiver_mac_add = "50:3e:aa:59:60:e7"
                        #receiver_mac_add = "a8:60:b6:10:be:a1"
                        # OUTGOING 
                        actions = [ act_set(ipv4_dst=fake_ip),
                                    act_set(ipv4_src=real_ip),
                                    act_set(tcp_dst=fake_port),
                                    act_set(eth_dst=receiver_mac_add),
                                   #act_out(self.mac_to_port[dp.id][receiver_mac_add]) ]
                                   act_out(1) ]
                        match = parser.OFPMatch(eth_type=0x0800,
                                                ipv4_dst=real_ip,
                                                ip_proto=6, #TCP,
                                                ipv4_src=self.recv_ip)
                        super(SimpleMonitor13, self).add_flow(dp, 15, match, actions)

                        # INCOMING  
                        actions = [
                            act_set(ipv4_src=real_ip),
                            act_set(ipv4_dst=self.recv_ip),
                            act_set(tcp_src=real_port),
                            act_set(eth_src=switch_mac_add),
                            act_set(eth_dst=sender_mac_add),
                            #act_out(self.mac_to_port[dp.id][sender_mac_add]) ]
                            act_out(4) ]
                        match = parser.OFPMatch(eth_type=0x0800,
                                                ipv4_src=fake_ip,
                                                ip_proto=6, #TCP,
                                                ipv4_dst=real_ip)
                        super(SimpleMonitor13, self).add_flow(dp, 25, match, actions)
            hub.sleep(5)

    def live_connection(self,hostname):

        def bool_parse(string):
            if string == "True":
                return True
            elif string == "False":
                return False
        url = hostname
        url = "64.90.52.128"
        url = "127.0.0.1:8000"
        command = "python ./connection_tester.py "+url
        print(command+"\n\n\n")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,shell=True)
        stringer = proc.communicate()[0][:-1]
        exit_code = proc.wait()
        print("\n\n\nENDING POLLER "+ str(stringer)+ "\n\n\n")
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

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        ip = pkt.get_protocol(ipv4.ipv4)
 
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        # LEARN MAC OF DPID,SRC COMBO
        if ip:
            self.ip_to_mac.setdefault(dpid, {})
            #print("\n\n\n"+str(ip)+"\n\n\n")
            # SET MAC TO IP MAPPING BASED ON SWITCH
            self.ip_to_mac[dpid][ip.src] = src
            self.ip_to_mac[dpid][ip.dst] = dst

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        prio=1
        #if (dst == constants.CONTROLLER_ETH) or (src == constants.CONTROLLER_ETH):
        # CATCH THE CONTROLLER MAC MY DUDE
        controller_eth = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
        if (dst == controller_eth) or (src == controller_eth):
            prio = 20

        # CATCH IF THE ETHERNET SOURCE IS THE SAMSUNG HUB
        hub_eth = constants.HUB_ETH
        if src == hub_eth:
            
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, prio, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, prio, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
