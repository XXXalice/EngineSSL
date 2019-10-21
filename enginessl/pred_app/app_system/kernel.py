import inspect
import os
import yaml

def preprocessing_judgement(pred):
    """
    前処理判断
    :param pred: model.predict()の戻り値
    :return: 未定
    """
    if pred[0].argmax() != 0:
        # 判断がnot_targetだったら
        params = read_yaml()
        bias_judgement(score=pred[0].max(), threshold=params['predictapp']['bias'])


def bias_judgement(score, threshold):
    pass


def read_yaml():
    here = '/'.join(inspect.stack()[0][1].split('/')[:-3])
    yaml_path = os.path.join(here, 'param.yml')
    with open(yaml_path, 'r') as d:
        param_dict = yaml.load(d)
    return param_dict
