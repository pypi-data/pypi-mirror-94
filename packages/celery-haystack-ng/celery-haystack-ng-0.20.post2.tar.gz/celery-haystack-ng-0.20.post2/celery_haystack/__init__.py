__version__ = '0.20.post2'


def version_hook(config):
    config['metadata']['version'] = __version__
