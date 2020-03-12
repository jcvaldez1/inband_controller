import docker
import main_controller
import requests
import traceback
from constants import DOCKER_DAEMON_URL, DOCKERFILE_PATH, DOCKER_HOST_IPV4,\
        DEFAULT_CONFIG_PORT
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
from container_wrapper import *
import json

class Docker_Handler(main_controller.SDN_Rerouter):

    def __init__(self, *args, **kwargs):
        super(Docker_Handler, self).__init__(*args, **kwargs)
        self.dockd = docker.DockerClient(base_url=DOCKER_DAEMON_URL)
        # cloud_ip : container_id
        self.container_list = [] 
        self.cloud_ip_list  = []
        self.command_cache = {}
        self.configuration_map = {}
        self.docker_image = self.dockd.images.build(path=DOCKERFILE_PATH)
        self.container_registrar = hub.spawn(self._main_manager)
        #self.configuration_poll  = hub.spawn(self._configuration_manager)
        #self.cleanup_handler    = hub.spawn(self._main_manager)

    def _main_manager(self):
        # check difference between container list
        # registered containers
        while(1):
            print("\ncontainer_list : "+str(self.container_list)+"\n")
            for alias_obj in self.aliases:
                print("MAPPY : " + str(alias_obj.real_port) + " " + str(alias_obj.cloud_ip) +" " + str(alias_obj.fake_port))
                if alias_obj.cloud_ip not in self.cloud_ip_list:
                    # get all alias_object instances
                    # containing this cloud_ip and retrieve
                    # their port information
                    port_list = self.retrieve_ports(alias_obj.cloud_ip)
                    container_obj = self.spin_up_container(alias_obj.cloud_ip, port_list, alias_obj.name)
                    self.cloud_ip_list.append(alias_obj.cloud_ip)
                    self.container_list.append(container_obj)
            hub.sleep(8)

    '''
           Manages each registered cloud and User ID pairs
           for configuration updates, and pushes them to each
           cloud
    '''
    def _configuration_manager(self):
        while(1):
            for container_obj in self.container_list:
                print("registered users : "+str(self.registered_users))
                print("cloud_ip : "+str(container_obj.cloud_ip))
                ### TENTATIVE ROUTE POSTING
                for alias in self.aliases:
                    print("MAPPY : " + str(alias.real_port) + " " + str(alias.cloud_ip) +" " + str(alias.fake_port))
                ### TENTATIVE ROUTE POSTING
                try:
                    configs = self.get_config_multi(container_obj.cloud_ip, self.registered_users)
                    print("configurations : "+str(configs))
                    # PUT requests.post, etc. to send configuration data to the DDH
                    self.send_config_data(configs, container_obj.config_path)
                except:
                    pass
                    #traceback.print_exc()
            hub.sleep(8)

    def retrieve_ports(self, cloud_ip):
        port_list = {}
        for alias_obj in self.aliases:
            if cloud_ip == alias_obj.cloud_ip:
                port_key = str(alias_obj.real_port)+"/tcp"
                port_list[port_key] = alias_obj.fake_port
        return port_list


    '''
            Finds a configuration path for a specific cloud_ip
    '''
    def find_config_path(self, cloud_ip):
        for alias in self.aliases:
            if ( alias.cloud_ip == cloud_ip ) and ( alias.real_port == DEFAULT_CONFIG_PORT ):
                return "http://"+str(DOCKER_HOST_IPV4)+":"+str(alias.fake_port)+"/config"
        return
        #return "http://"+str(cloud_ip)+":"+str(DEFAULT_CONFIG_PORT)
        
    def send_config_data(self, configuration_data, config_path):
        response = requests.post(config_path, json={'config':json.dumps(configuration_data)}) 
        return response.text

    def update_from_deviceID(self, cloud_address, deviceID):
        response = requests.get('http://'+cloud_address+'/return_config',params={'deviceID':deviceID}) 
        return response.text

    def get_config_multi(self, cloud_address, group):
        response = requests.get('http://'+cloud_address+'/return_group_config_multi',json={'group':group})
        print(str(response))
        print(str(response.text))
        return response.text
   
    def get_devices_in_group(self, cloud_address, group):
        response = requests.get('http://'+cloud_address+'/return_group',params={'group':group})
        return response.text
   
    def get_group_config(self, cloud_address, group):
        response = requests.get('http://'+cloud_address+'/return_group_config',params={'group':group})
        return response.text

    def deliver_config_to_container(self, container_config_port, config_to_deliver):
        response = requests.post('http://'+DOCKER_HOST_IPV4+':'+container_config_port+'/config',json=config_to_deliver)
        return response.text

    def spin_up_container(self, cloud_ip, ports, name):
        container = self.dockd.containers.run(image=self.docker_image[0],detach=True,network='docknet',hostname=cloud_ip, name=name, ports=ports)
        config_path = self.find_config_path(cloud_ip)
        print("CONFIG PATH FOR " +str(cloud_ip) + " : " + str(config_path))
        container_obj = DDH_Container(config_path  = config_path, 
                                      cloud_ip     = cloud_ip,
                                      name         = name,
                                      container_id = container.id)
        return container_obj
        # return the ran container object
    


#dhh = Docker_Handler()
#print(dhh.update_from_deviceID('52.74.73.81','RPI'))
