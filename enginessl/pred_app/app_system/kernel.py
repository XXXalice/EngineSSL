import inspect
import os
import yaml

def bias_judgement(score):
    pass


def read_yaml():
    here = '/'.join(inspect.stack()[0][1].split('/')[:-3])
    yaml_path = os.path.join(here, 'param.yml')
    with open(yaml_path, 'r') as d:
        param_dict = yaml.load(d)
    return param_dict
