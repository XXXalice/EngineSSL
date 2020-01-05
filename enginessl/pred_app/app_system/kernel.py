import inspect
import os
import yaml

def preprocessing_judgement(pred, bias):
    """
    前処理判断
    :param pred: model.predict()の戻り値
    :return: 未定
    """

    # 判断がtargetだったら
    if pred[0].argmax() == 0:
        result = bias_judgement(score=max(pred[0]), threshold=bias)
    else:
        result = 'not_target'
    return result


def bias_judgement(score, threshold):
    print(score)
    if score >= float(threshold) / 100:
        return 'target'
    else:
        return 'not_target'


def read_yaml():
    here = '/'.join(inspect.stack()[0][1].split('/')[:-3])
    yaml_path = os.path.join(here, 'param.yml')
    with open(yaml_path, 'r') as d:
        param_dict = yaml.load(d)
    return param_dict
