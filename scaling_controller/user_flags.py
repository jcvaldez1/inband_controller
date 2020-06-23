from ryu import cfg

CONF = cfg.CONF
CONF.register_cli_opts([ cfg.StrOpt( 'conf', default="default.py",
                                    help='specify config file to be used'),])

