import numpy as np
import sys
import os
import glob
from keras.preprocessing.image import load_img, img_to_array, array_to_img, save_img , ImageDataGenerator
from keras.utils import to_categorical
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from common_handler.path_handler import get_path_with_glob

# Generate conflicting images fully automatically :)

# [usage]
# 2 step (Please set param.yaml in advance.)
#
# instance = OpponentImage(Kernel):
# instance.return_datafile()
#
# too easy ! :)

class Kernel():

    def __init__(self):
        exec_path = os.path.dirname(os.path.abspath(__file__))
        base = 'enginessl'
        datas_dir = get_path_with_glob(exec_path, base, 'data/img')
        if '.DS_Store' in datas_dir:
            datas_dir.remove('.DS_Store')
        try:
            self.labels = list(map(lambda label: label.split('_')[0], datas_dir))
            self.params = self.read_yaml(get_path_with_glob(exec_path, base, 'param.yml'))
            self.datas = glob.glob('**' + datas_dir[0] + '/*.{}'.format(self.params['crawler']['ext']))
            self.datas.sort()
        except Exception as e:
            sys.stderr.write(str(e))
            print("error cant read datas.")
            exit()

    def data_split(self, validation=False):
        test_num = int(len(self.datas) * self.params['ml']['test_data_rate'])
        train_num = len(self.datas) - test_num
        self.x_train_raw = self.datas[:train_num]
        self.x_test_raw = self.datas[-test_num:]

    def data_preprocess_basic(self, gray=True, size=(100,100), precision=np.float32):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        size = [self.params['ml']['img_size_xy']]*2 if not self.params['ml']['img_size_xy'] == None else size
        for label, valid in enumerate([self.x_train_raw, self.x_test_raw]):
            for img_path in valid:
                try:
                    img = load_img(img_path, grayscale=gray, target_size=tuple(size))
                    img_bin = img_to_array(img)
                    # data_container[label].append(img_bin)
                    if label == 0:
                        self.x_train.append(img_bin)
                        self.y_train.append([0])
                    elif label == 1:
                        self.x_test.append(img_bin)
                        self.y_test.append([0])
                except:
                    print('cant preprocessed image.[{}]'.format(img_path))
                    continue
                else:
                    print('encoded img.[{}]'.format(img_path))
            # self.x_train = list(map(lambda img_bin: np.float16(img_bin)/255, self.x_train))
            # self.x_test = list(map(lambda img_bin: np.float16(img_bin) / 255, self.x_test))
            self.x_train = list(map(lambda img_bin: np.ravel(precision(img_bin) / 255), self.x_train))
            self.x_test = list(map(lambda img_bin: np.ravel(precision(img_bin) / 255), self.x_test))
        print('data shape {}'.format(self.x_train[0].shape))
        print('train {}  test {}'.format(len(self.x_train), len(self.x_test)))

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
        self.ancestors = [self.x_train, self.x_test]
        self.ancestors_label = [self.y_train, self.y_test]
        self.decay = self.params['oppoimg']['decay']
        self.mode = self.params['oppoimg']['mode']
        # self.__gc_superclassvals()
        self.datas = self.make_fuzzyimg(decay=self.decay, effect=self.mode)

    def make_fuzzyimg(self, decay, effect):
        from . import effect_func as ef

        e_dict = {
            's_random': lambda x: ef.simple_random(x),
            'swap': lambda x: ef.swap(x),
            'as_random': lambda  x: ef.ancestral_scale_random(x),
            'as_randomv2': lambda x: ef.ancestral_scale_random_v2(x)
        }

        for i, img_bins in enumerate(self.ancestors):
            flat_img_bins = [*map(lambda img_bin: np.ravel(img_bin), img_bins)]
            for img_count, flat_img_bin in enumerate(flat_img_bins):
                # print(flat_img_bin, flat_img_bin.shape)
                # break
                try:
                    effected_bin = e_dict[effect](flat_img_bin)
                    # self.ancestors[i].append(effected_bin)
                    # self.ancestors_label[i].append([1])
                    if i == 0:
                        self.x_train.append(effected_bin)
                        self.y_train.append([1])
                    elif i == 1:
                        self.x_test.append(effected_bin)
                        self.y_test.append([1])
                except:
                    print('cant generate fuzzyimg.')
                    continue
                else:
                    print('generated fuzzyimg. num:{}'.format(img_count+1))
        print('fuzzy mode {}'.format(effect))
        # self.test_show(self.ancestors[0][150])

    def anal_ances(self):
        pass

    def return_datafiles(self):
        self.y_train = to_categorical(self.y_train, num_classes=2)
        self.y_test = to_categorical(self.y_test, num_classes=2)
        return (self.x_train, self.x_test, self.y_train, self.x_test)

    def test_show(self, np_img):
        import matplotlib.pyplot as plt
        ex_img = array_to_img(np_img.reshape(100,100,1))
        ex_img.save('test.png')

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
    k = Kernel()
    # k.data_split()
    # k.data_preprocess_basic()
    # oppi = OpponentImage()
    # datasets = oppi.return_datafiles()