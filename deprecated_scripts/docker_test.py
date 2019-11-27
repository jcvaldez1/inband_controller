import docker

NETWORK_NAME = "dockerstuff_default"
client = docker.from_env()
networks = client.networks
container_network = None
for x in networks.list():
    if x.name == NETWORK_NAME:
        print(x.name)
        container_network = x
        break

new_container = client.containers.run('bfirsh/reticulate-splines',detach=True)
container_network.connect(new_container)

