import docker
from flask import Flask, request
import json

application = Flask(__name__)
client = docker.from_env()
piccy = client.images.build(
    path="/home/pi/Desktop/Docker"
)


@application.route("/register/", methods=["POST"])
def receive():
    args = request.get_json()
    
    client.containers.run(
        image=piccy[0],
        detach=True,
        network="docknet",
        hostname=args["name"],
        name=args["name"],
        ports=args["ports"]
    )
    print("number of containers: "+ str(len(client.containers.list(all=True))))
    return "ok cool"


if __name__ == "__main__":

    application.run(host="0.0.0.0", port=8000)
