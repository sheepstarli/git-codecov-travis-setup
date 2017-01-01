import yaml
import os

__all__ = [
    'get_config'
]

__author__ = 'sheepstarli <licx@easemob.com>'


def read_yaml_config():
    config_file = file(os.path.expanduser('~') + '/gcts-config.yaml', 'r')
    # config_file = file('gcts-config.yaml', 'r')
    yaml_config = yaml.load(config_file)
    return yaml_config
