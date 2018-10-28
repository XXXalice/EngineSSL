import numpy as np
import glob
import sys
import os
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator

class Kernel():

    def __init__(self):
        datas_path = '../../data/img/'
        datas_dir = os.listdir(path=datas_path)
        if '.DS_Store' in datas_dir:
            datas_dir.remove('.DS_Store')
        try:
            self.labels = list(map(lambda label: label.split('_')[0], datas_dir))
            self.params = self.read_yaml('../../param.yml')
            self.datas = glob.glob(datas_path + datas_dir[0] + '/*.{}'.format(self.params['crawler']['ext']))
            self.datas.sort()
        except Exception as e:
            sys.stderr.write(str(e))
            print()
            exit()

    def data_split(self, validation=False):
        test_num = int(len(self.datas) * self.params['ml']['test_data_rate'])
        train_num = len(self.datas) - test_num
        self.x_train_raw = self.datas[:train_num]
        self.x_test_raw = self.datas[-test_num:]

    def data_preprocess_basic(self, gray=True, size=(100,100)):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        data_container = [self.x_train, self.x_test]
        label_container = [self.y_train, self.y_test]
        size = [self.params['ml']['img_size_xy']]*2 if not self.params['ml']['img_size_xy'] == None else size
        for label, valid in enumerate((self.x_train_raw, self.x_test_raw)):
            for img_path in valid:
                try:
                    img = load_img(img_path, grayscale=gray, target_size=tuple(size))
                    img_bin = img_to_array(img)
                    data_container[label].append(img_bin)
                    label_container[label].append(0)
                except:
                    print('cant preprocessed image.[{}]'.format(img_path))
                    continue
                else:
                    print('encoded img.[{}]'.format(img_path))
            self.x_train = list(map(lambda img_bin: np.float16(img_bin)/255, self.x_train))
            self.x_test = list(map(lambda img_bin: np.float16(img_bin) / 255, self.x_test))
        print('data shape {}'.format(self.x_train[0].shape))

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


from PIL import Image, ImageChops, ImageOps, ImageDraw

#generate image of opponent
class OpponentImage(Kernel):

    def __init__(self):
        Kernel.__init__(self)
        self.data_split()
        self.data_preprocess_basic()
        self.ancestors = [self.x_train, self.y_train, self.x_test, self.y_test]
        # self.__gc_superclassvals()

    def make_fuzzyimg(self, decay):
        pass

    def __gc_superclassvals(self):
        import gc
        rm_ivals = [ival for ival in list(self.__dict__.keys()) if ival is not 'ancestors']
        for rm_ival in rm_ivals:
            try:
                del rm_ival
            except Exception as e:
                print(e)
                exit()


# kernel test
if __name__ == '__main__':
    # k = Kernel()
    # k.data_split()
    # k.data_preprocess_basic()
    oppi = OpponentImage()