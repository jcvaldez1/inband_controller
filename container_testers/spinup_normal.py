import docker
import requests
import traceback
import time
from constants import DOCKER_DAEMON_URL, DOCKERFILE_PATH, DOCKER_HOST_IPV4,\
        DEFAULT_CONFIG_PORT
import json
import sys

def spin_up_container(docker_client, image):
    container = docker_client.containers.run(image=image,detach=True,network='docknet')
    return container


if __name__ == "__main__":
    dockd = docker.DockerClient(base_url=DOCKER_DAEMON_URL)
    docker_image = dockd.images.build(path=DOCKERFILE_PATH)
    conts = []
    for x in range(0, int(sys.argv[1])+1):
        cont = spin_up_container(dockd, docker_image[0])
        conts.append(cont)
        print(str(x)+" : "+str(cont))
