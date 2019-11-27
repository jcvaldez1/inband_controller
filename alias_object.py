'''
        Alias object for storing info about a registered
        entry of a cloned cloud service in the DDH
        @ATTRIBUTES:
            real_port   : the real destination TCP port to be used
                          by the IoT device

            fake_port   : the TCP port of the DDH to be exposed for
                          network traffic corresponding to the value of 
                          real_port
            cloud_ip    : the IPv4 address of the cloud service to be 
                          cloned via a docker container in the DDH
'''
class Alias(object):
    def __init__(self, *args, **kwargs):
        super(Alias, self).__init__()
        self.real_port = kwargs['real_port']
        self.fake_port = kwargs['fake_port']
        self.cloud_ip = kwargs['cloud_ip']

