import inspect
import os
from . import kernel as mlkernel
from . import network

class MachineLearning(mlkernel.Kernel):

    def __init__(self):
        param_path = os.path.join('/'.join(inspect.stack()[0][1].split('/')[:-2]), 'param.yml')
        self.Ml = mlkernel.Kernel(param_path)

    def get_datas(self):
        '''
        :return: tuple(x_train, x_test, y_train, y_test)
        '''
        self.datas = self.Ml.get_origin_data()
        return self.datas

    def get_preprocessed_data(self):
        '''
        :return: tuple(x_train, x_test, y_train, y_test) #分割済み
        '''
        self.datas = self.Ml.correct_datas()
        return self.datas

    def build_model(self):
        self.model = self.Ml.generate_model()
        return self.model

    def train_model(self, model, datas, save_name):
        return self.Ml.training(model=model, datas=datas, save_name=save_name)

    def fine_tuning_model(self):
        pass

