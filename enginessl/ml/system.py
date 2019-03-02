from . import kernel as mlkernel
from . import network

class MachineLearning(mlkernel.Kernel):

    def __init__(self, param_path='param.yml'):
        self.Ml = mlkernel.Kernel(param_path)

    def get_datas(self):
        '''
        :return: tuple(self.x_train, self.x_test, self.y_train, self.y_test)
        '''
        self.datas = self.Ml.get_origin_data()
        return self.datas

    def build_model(self):
        self.model = self.Ml.generate_model()
        return self.model

    def train_model(self, model, datas):
        self.Ml.training(model=model, datas=datas)

    def fine_tuning_model(self):
        pass