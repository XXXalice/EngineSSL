import numpy as np
import glob
import sys
import os
from keras.preprocessing.image import load_img, img_to_array

class Kernel():
    def __init__(self):
        datas_path = '../../data/img/'
        try:
            self.labels = list(map(lambda label: label.split('_')[0], os.listdir(path=datas_path)))
            self.datas = glob.glob(datas_path + os.listdir(path=datas_path)[0] + '/*.png')
            self.params = self.read_yaml('../../param.yml')
        except Exception as e:
            sys.stderr.write(str(e))
            print()
            exit()

    def data_split(self, validation=False):
        test_num = int(len(self.datas) * self.params['ml']['test_data_rate'])
        train_num = len(self.datas) - test_num
        self.x_train_raw = self.datas[:train_num]
        self.x_test_raw = self.datas[-test_num:]


    def data_preprocess(self,gray=True):
        pass

    def labeling(self, one_hot=True):
        pass

    def read_yaml(self, uri):
        import yaml
        try:
            with open(uri, 'r') as d:
                param_dict = yaml.load(d)
        except Exception as err:
            sys.stdout.write(str(err))
            return
        return param_dict




# kernel test
if __name__ == '__main__':
    k = Kernel()
    k.data_split()