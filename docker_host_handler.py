import docker
import main_controller
from constants import DOCKER_DAEMON_URL

class Docker_Handler(main_controller.SDN_Rerouter):

    def __init__(self, *args, **kwargs):
        super(Docker_Handler, self).__init__(*args, **kwargs)
        self.dockd = docker.DockerClient(base_url=DOCKER_DAEMON_URL)
        self.server_list = {} 

'''
    EVERYTHING DOCKER DAEMON RELATED GOES HERE
'''

    def test_func(self):
        pass
