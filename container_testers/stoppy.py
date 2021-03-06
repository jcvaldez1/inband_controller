import docker
import requests
import traceback
import time
import statistics
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
    times = []
    for x in range(0, int(sys.argv[1])+1):
        cont = spin_up_container(dockd, docker_image[0])
        conts.append(cont)
        print(str(x)+" : "+str(cont))
        cont.stop()
        print(str(x)+" stopped")

    count = 0
    up_num = int(sys.argv[2])
    for c in conts:
        pre_pause = time.time()
        c.start()
        total_time = time.time() - pre_pause
        times.append(total_time)
        print("unstopped "+str(count))
        count+=1
        if count >= up_num:
            conts[count-up_num].stop()
            print(str(count-up_num)+" stopped")


    try:
        print("mean : "+str(statistics.mean(times)))
        print("median : "+str(statistics.median(times)))
        print("mode : "+str(statistics.mode(times)))
    except:
        pass
