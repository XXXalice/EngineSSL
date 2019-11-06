import inspect
import os
from . import kernel as mlkernel

class MachineLearning(mlkernel.Kernel):

    def __init__(self):
        param_path = os.path.join('/'.join(inspect.stack()[0][1].split('/')[:-2]), 'param.yml')
        self.ml = mlkernel.Kernel(param_path)
        self.user_nn = self.ml.user_nn

    def build_model(self, num_classes):
        self.model = self.user_nn.generate_model(num_classes=num_classes)
        return self.model

    def train(self, name, model, datas, es):
        return self.user_nn.train(name=name ,model=model, datas=datas, es=es)

    def draw_graph(self, model_name):
        self.draw_graph(model_name=model_name)

    def fine_tuning_model(self):
        pass

