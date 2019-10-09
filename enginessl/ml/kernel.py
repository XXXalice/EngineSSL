import sys
import os
from keras.applications import MobileNetV2
from keras.layers import Input

class Kernel():

    def __init__(self, param_path):
        self.params = self.read_yaml(param_path)
        self.wh = self.params['ml']['img_size_xy'] #正方形
        self.using_user_network = False
        if self.params['ml']['model'] == 'origin':
            self.using_user_network = True
            if self.params['ml']['use_easymode'] == True:
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                import network_easymode_highspeed
                self.user_nn = network_easymode_highspeed.NetworkHighspeed(self.params)
            else:
                from . import network
                self.user_nn = network.TestNet(self.params)
        self.ances_model = None
        self.train_data = None

    def generate_model(self, app='MobileNetV2'):
        #easymodeがオンになって居た場合それを使用する
        if self.params['ml']['use_easymode'] == True:
            return self.user_nn.build_model()

        save_path_master = './models/'
        exec_dict = {
            'MobileNetV2': lambda tensor_shape: __mbnv2(tensor_shape),
        }

        def __mbnv2(tensor_shape):
            try:
                input_tensor = Input(shape=tensor_shape)
                loaded_model = MobileNetV2(include_top=False, weights='imagenet')
                # loaded_model = MobileNetV2(include_top=False, weights='imagenet', input_tensor=input_tensor)
            except Exception as err:
                print('cant load model. plz check your tensorflow and Keras version.')
                sys.stdout.write(str(err))
                exit()
            else:
                return loaded_model

        if self.read_tensor_shape(self.train_data[0][0]) == True and not os.path.exists(save_path_master + app + '.' + self.params['ml']['savemodel_ext']):
            self.ances_model = exec_dict[app](self.train_data[0][0].shape)
            self.ances_model.save(save_path_master + app + '.' + self.params['ml']['savemodel_ext'])

    def read_tensor_shape(self, ex):
        try:
            self.tensor_shape = ex.shape
        except Exception as err:
            print('cant read preprocessed images shape. plz check exection file.')
            sys.stdout.write(str(err))
        else:
            return True

    def training(self, model, datas, save_name, es):
        return self.user_nn.train(model=model, preprocessing_datas=datas, save_name=save_name, es=es)

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

    def get_origin_data(self, save_testimg=True):
        from .data_handling import system as dh_api
        try:
            dh = dh_api.DataHandling()
            origin_data = dh.get_builtup_data()
            if save_testimg == True:
                dh.test_show(origin_data[0][-1])
            return origin_data
        except Exception as err:
            sys.stdout.write(str(err))
            return