import docker
import main_controller
import requests
from constants import DOCKER_DAEMON_URL, DOCKERFILE_PATH

class Docker_Handler(main_controller.SDN_Rerouter):

    def __init__(self, *args, **kwargs):
        super(Docker_Handler, self).__init__(*args, **kwargs)
        self.dockd = docker.DockerClient(base_url=DOCKER_DAEMON_URL)
        self.server_list = {} 
        self.command_cache = {}
        self.docker_image = self.dockd.build(path=DOCKERFILE_PATH)

    def update_from_deviceID(self,cloud_address,deviceID):
        response = requests.get('http://'+cloud_address+'/return_config',params={'deviceID':deviceID}) 
        return response.text

    def get_devices_in_group(self,cloud_address,group):
        response = requests.get('http://'+cloud_address+'/return_group',params={'group':group})
        return response.text
    
    def spin_up_container(self,name,ports):
        self.dockd.run(image=self.docker_image[0],detach=True,network='docknet',hostname=name,ports=ports)
    


dhh = Docker_Handler()
print(dhh.update_from_deviceID('52.74.73.81','RPI'))
