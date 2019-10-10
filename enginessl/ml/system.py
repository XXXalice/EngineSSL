import inspect
import os
from . import kernel as mlkernel
from . import network

class MachineLearning(mlkernel.Kernel):

    def __init__(self):
        param_path = os.path.join('/'.join(inspect.stack()[0][1].split('/')[:-2]), 'param.yml')
        self.ml = mlkernel.Kernel(param_path)
        self.user_nn = self.ml.user_nn

    def build_model(self, datas):
        self.model = self.user_nn.generate_model(datas=datas)
        return self.model

    def train_model(self, model, datas, save_name, es=True):
        save_name = save_name.split('_')[0]
        return self.ml.training(model=model, datas=datas, save_name=save_name, es=es)

    def fine_tuning_model(self):
        pass

