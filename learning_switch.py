# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
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

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
import re, uuid, json, sys
import docker
import requests
from constants import DOCKER_DAEMON_URL, DOCKER_HOST_ETH, \
        REGISTRATION_IP, CONTROLLER_ETH, FORWARDING_TABLE,\
        DEFAULT_TABLE, REROUTING_TABLE, DEFAULT_PORT_COUNTER,\
        CONTROLLER_TABLE
from alias_object import Alias
import traceback

'''
        BaseSwitch is a directly modified version of the
        provided SimpleSwitch13 class from Ryu. It provides
        basic switch capabilities and has the resources to be
        used for most of the further capabilities to be developed

        @ATTRIBUTES
            mac_to_port     : key value map of mac addresses to their
                              corresponding port number ON THE SWITCH
            ip_to_mac       : key value map of ipv4 addresses to their
                              corresponding mac addresses
            used_ports      : list of currently used TCP ports by the 
                              Dedicated Docker Host
            port_counter    : an integer used to show the current highest
                              available TCP port number of the DDH, assume
                              all port numbers equal or higher than this
                              value is available and all port numbers below
                              it are in use
'''
class BaseSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(BaseSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.ip_to_mac = {}
        #self.docker_daemon = docker.from_env()
        #self.main_network = self.register_network("dockerstuff_default")

    #def register_network(self, network_name):
    #    networks = self.docker_daemon.networks
    #    for network in networks.list():
    #        if network.name == network_name:
    #            return network
    #    return


    '''
            changds were added from_controller parameters to the
            add_flow() function calls in order to remove hard
            timeouts to the flows made by this handler
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        actions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        self.add_flow(datapath, CONTROLLER_TABLE, 0, match, actions, None, True)

        # default table
        actions = [parser.OFPInstructionGotoTable(REROUTING_TABLE)]
        self.add_flow(datapath, DEFAULT_TABLE, 1, match, actions, None, True)

    '''
            changes were only hard timeouts added to every flow 
            except controller flows
    '''
    def add_flow(self, datapath, table_id, priority, match, inst, buffer_id=None, from_controller=False):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        hrd_tm = 10
        if from_controller:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, table_id=table_id)
        else:
            if buffer_id:
                mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                        priority=priority, match=match,
                                        instructions=inst, table_id=table_id,
                                        hard_timeout=hrd_tm)
            else:
                mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                        match=match, instructions=inst,
                                        table_id=table_id, hard_timeout=hrd_tm)
        datapath.send_msg(mod)

    '''
            changes include having a call to device registration
    '''
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
            if ip.dst == REGISTRATION_IP:
                self.register_device(pkt.protocols[-1])
            self.ip_to_mac[dpid][ip.src] = src
            self.ip_to_mac[dpid][ip.dst] = dst

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            self.logger.info("packet in %s %s FLOODED",  src, dst)
            self.logger.info("mac_to_port : %s",  self.mac_to_port)
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        prio=1
        # RETRIEVE CONTROLLER HOST HARDWARE ADDRESS
        controller_eth = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
        if (dst == controller_eth) or (src == controller_eth):
            prio = 20

        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, FORWARDING_TABLE, prio, match, inst, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, FORWARDING_TABLE, prio, match, inst)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

