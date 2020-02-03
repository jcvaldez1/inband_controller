import docker
from flask import Flask, request
import json
import time

application = Flask(__name__)
client = docker.from_env()
piccy = client.images.build(
    path="/home/dedicated-docker-host/Desktop/dockerstuff"
)
avg_time=[]


@application.route("/register/", methods=["POST"])
def receive():
    args = request.get_json()
    start_time = time.time()
    client.containers.run(
        image=piccy[0],
        detach=True,
        network="docknet",
        hostname=args["name"],
        name=args["name"],
        ports=args["ports"]
    )
    speed = time.time() - start_time
    print("--- %s seconds ---" % (speed))
    outfile = open('averages.txt','a')
    outfile.write(str(speed)+'\n')
    outfile.close()
    avg_time.append(speed)
    print("avg time: %s" % (sum(avg_time)/len(avg_time)))
    
    print("container count: "+str(len(client.containers.list(all=True))))
    return "ok boomer"


if __name__ == "__main__":
    # client is docker daemon
    # check network first for docknet network
    if not client.networks.list(names="docknet"):
        client.networks.create("docknet", driver="bridge")
    application.run(host="0.0.0.0", port=8000)
