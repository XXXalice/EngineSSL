import sys
import os
from keras.models import Sequential, Model
from keras.applications import MobileNetV2
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras import optimizers

class Kernel():

    def __init__(self, train_data):
        self.params = self.read_yaml('../param.yml')
        self.wh = self.params['ml']['img_size_xy'] #正方形
        self.ances_model = None
        self.train_data = train_data

    def generate_model(self, app='MobileNetV2'):

        save_path_master = './models/'
        exec_dict = {
            'MobileNetV2': lambda tensor_shape: __mbnv2(tensor_shape),
        }

        def __mbnv2(tensor_shape):
            try:
                loaded_model = MobileNetV2(include_top=False, weights='imagenet', input_tensor=tensor_shape)
            except Exception as err:
                print('cant load model. plz check your tensorflow and Keras version.')
                sys.stdout.write(str(err))
                exit()
            else:
                return loaded_model

        if self.read_tensor_shape(self.train_data[0][0]) is True and not os.path.exists(save_path_master + app + self.params['ml']['savemodel_ext']):
            self.ances_model = exec_dict[app]()
            self.ances_model.save(save_path_master + app + self.params['ml']['savemodel_ext'])

    def read_tensor_shape(self, ex):
        try:
            self.tensor_shape = ex.shape
        except Exception as err:
            print('cant read preprocessed images shape. plz check exection file.')
            sys.stdout.write(str(err))
        else:
            return True

    def fine_tuning(self):
        #dense
        if not self.ances_model is None:
            pass
        else:
            print('cant read ancestormodel.')
            exit()

    def read_yaml(self, uri):
        import yaml
        try:
            with open(uri, 'r') as d:
                param_dict = yaml.load(d)
        except Exception as err:
            sys.stdout.write(str(err))
            return
        return param_dict


#test kernel
if __name__ == '__main__':
    from data_handling.system import DataHandling
    d = DataHandling()
    datas = d.get_builtup_data()
    k = Kernel(datas)
    k.generate_model()