class DDH_Container(object):
    def __init__(self, *args, **kwargs):
        super(DDH_Container, self).__init__()
        self.config_path = kwargs['config_path']
        self.cloud_ip = kwargs['cloud_ip']
        self.name = kwargs['name']
        self.container_id = kwargs['container_id'] 

