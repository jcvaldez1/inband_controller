import docker
import pprint as pp

NETWORK_NAME = "dockerstuff_default"
client = docker.from_env()
con_net = None
for x in client.networks():
    if x['Name'] == NETWORK_NAME:
        con_net = x
        break

pp.pprint(dir(client))
new_container = client.create_container('bfirsh/reticulate-splines',detach=True)
client.start(new_container)
pp.pprint(dir(new_container))
pp.pprint(dir(con_net))
pp.pprint(con_net)
client.connect_container_to_network(new_container,con_net["Id"])
#con_net.connect(new_container)
