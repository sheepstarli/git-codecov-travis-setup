import yaml
import os

__all__ = [
    'get_config'
]

__author__ = 'sheepstarli <licx@easemob.com>'


def read_yaml_config():
    config_file = file(os.path.expanduser('~') + '/gcts-config.yml', 'r')
    # config_file = file('gcts-config.yml', 'r')
    yaml_config = yaml.load(config_file)
    return yaml_config
