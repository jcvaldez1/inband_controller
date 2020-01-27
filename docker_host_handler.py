import docker
import main_controller
import requests
import traceback
from constants import DOCKER_DAEMON_URL, DOCKERFILE_PATH, DOCKER_HOST_IPV4
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

class Docker_Handler(main_controller.SDN_Rerouter):

    def __init__(self, *args, **kwargs):
        super(Docker_Handler, self).__init__(*args, **kwargs)
        self.dockd = docker.DockerClient(base_url=DOCKER_DAEMON_URL)
        #print(self.dockd.images.list())
        # cloud_ip : container_id
        self.container_list = {} 
        self.command_cache = {}
        self.docker_image = self.dockd.images.build(path=DOCKERFILE_PATH)
        self.checker_thread = hub.spawn(self._main_manager)

    def _main_manager(self):
        # check difference between container list
        # registered containers
        while(1):
            print("\ncontainer_list : "+str(self.container_list)+"\n")
            for alias_obj in self.aliases:
                if alias_obj.cloud_ip not in self.container_list:
                    # get all alias_object instances
                    # containing this cloud_ip and retrieve
                    # their port information
                    port_list = self.retrieve_ports(alias_obj.cloud_ip)
                    container_id = self.spin_up_container(alias_obj.cloud_ip, port_list, alias_obj.name)
                    self.container_list[alias_obj.cloud_ip] = container_id
            hub.sleep(8)

    def retrieve_ports(self, cloud_ip):
        port_list = {}
        for alias_obj in self.aliases:
            if cloud_ip == alias_obj.cloud_ip:
                port_key = str(alias_obj.real_port)+"/tcp"
                port_list[port_key] = alias_obj.fake_port
        return port_list


    def update_from_deviceID(self,cloud_address,deviceID):
        response = requests.get('http://'+cloud_address+'/return_config',params={'deviceID':deviceID}) 
        return response.text

    def get_devices_in_group(self,cloud_address,group):
        response = requests.get('http://'+cloud_address+'/return_group',params={'group':group})
        return response.text
   
    def deliver_config_to_container(self,container_config_port,config_to_deliver):
        response = requests.post('http://'+DOCKER_HOST_IPV4+':'+container_config_port+'/config',json=config_to_deliver)
        return response.text

    def spin_up_container(self, cloud_ip, ports, name):
        container = self.dockd.containers.run(image=self.docker_image[0],detach=True,network='docknet',hostname=cloud_ip, name=name, ports=ports)
        return container.id
        # return the ran container object
    


#dhh = Docker_Handler()
#print(dhh.update_from_deviceID('52.74.73.81','RPI'))
