import testboi

class RemoverBoy(testboi.SimpleSwitch13):
    def remove_table_flows(self, datapath, table_id, match, instructions):
        """Create OFP flow mod message to remove flows from table."""
        ofproto = datapath.ofproto
        flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, table_id,f proto.OFPFC_DELETE,
0,0,1,ofproto.OFPCML_NO_BUFFER,ofproto.OFPP_ANY,OFPG_ANY, 0,match, instructions)
        return flow_mod



empty_match = parser.OFPMatch()
instructions = []
flow_mod = self.remove_table_flows(datapath, 0,empty_match, instructions)
print "deleting all flow entries in table ", 0
datapath.send_msg(flow_mod)
