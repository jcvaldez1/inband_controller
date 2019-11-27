import docker

client = docker.from_env()
client.networks.list()
