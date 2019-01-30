import numpy as np
import sys
import os
import glob
from keras.preprocessing.image import load_img, img_to_array, array_to_img, save_img , ImageDataGenerator
from keras.utils import to_categorical
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from common_handler.path_handler import get_path_with_glob, get_abspath_with_glob
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
        self.exec_path = os.path.dirname(os.path.abspath(__file__))
        base = 'enginessl'
        img_dir = 'data/img'
        datas_dir = get_path_with_glob(self.exec_path, base, img_dir)
        if '.DS_Store' in datas_dir:
            datas_dir.remove('.DS_Store')
        try:
            self.labels = list(map(lambda label: label.split('_')[0], datas_dir))
            self.params = self.read_yaml(get_path_with_glob(self.exec_path, base, 'param.yml'))
            # self.datas = get_path_with_glob(exec_path, base, '.+datas_dir[0] + '/*.{}'.format(self.params['crawler']['ext']))
            self.img_dir_abspath = os.path.join(self.exec_path.split(base)[0], base, img_dir, datas_dir[0])
            self.datas = [self.img_dir_abspath + '/' + img_name for img_name in get_path_with_glob(self.exec_path, base, datas_dir[0])]
            self.datas.sort()
        except Exception as e:
            sys.stderr.write(str(e))
            print("error cant read datas.")
            exit()
        else:
            pass
        #     import pprint
        #     pprint.pprint(self.datas)

    def data_split(self, validation=False):
        try:
            test_num = int(len(self.datas) * self.params['ml']['test_data_rate'])
            train_num = len(self.datas) - test_num
            self.x_train_raw = self.datas[:train_num]
            self.x_test_raw = self.datas[-test_num:]
        except Exception as err:
            sys.stdout.write(str(err))
        else:
            print('splited datas. test:{test}  train:{train}'.format(test=len(self.x_train_raw), train=len(self.x_test_raw)))

    def data_preprocess_basic(self, gray=True, size=(100,100), precision=np.float32):
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        size = [self.params['ml']['img_size_xy']]*2 if not self.params['ml']['img_size_xy'] == None else size
        for label, valid in enumerate([self.x_train_raw, self.x_test_raw]):
            for img_path in valid:
                try:
                    img = load_img(img_path, color_mode='grayscale', target_size=tuple(size))
                    img_bin = img_to_array(img)
                    # data_container[label].append(img_bin)
                    if label == 0:
                        self.x_train.append(img_bin)
                        self.y_train.append([0])
                        print('encoded img for train.[{}]'.format(img_path))
                    elif label == 1:
                        self.x_test.append(img_bin)
                        self.y_test.append([0])
                        print('encoded img for test.[{}]'.format(img_path))
                except:
                    print('cant preprocessed image.[{}]'.format(img_path))
                    continue
                else:
                    pass
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

    def make_fuzzyimg(self, decay, effect, img_save=True):
        import effect_func as ef

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
                    if img_save == True:
                        self.save_fuzzyimg(np_img=effected_bin, num=img_count+1)
                    print('generated fuzzyimg. num:{}'.format(img_count+1))
        print('fuzzy mode {}'.format(effect))
        # self.test_show(self.ancestors[0][150])

    def save_fuzzyimg(self, np_img, num):
        absdatas_dir = get_abspath_with_glob(self.exec_path, 'data')
        if '.DS_Store' in absdatas_dir:
            absdatas_dir.remove('.DS_Store')
        if not os.path.exists(absdatas_dir[0] + '/fuzzies'):
            os.mkdir(absdatas_dir[0] + '/fuzzies')
        elif not os.path.exists(os.path.join(absdatas_dir[0], 'fuzzies', get_path_with_glob(self.exec_path, 'enginessl', 'img'))):
            fuzzies_dir = os.path.join(absdatas_dir[0], 'fuzzies', get_path_with_glob(self.exec_path, 'enginessl', 'img'))
            os.mkdir(fuzzies_dir)
        ex_img = array_to_img(np_img.reshape(100,100,1))
        ex_img.save(os.path.join(fuzzies_dir, '{0:03d}.png'.format(num)))

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
    oppi = OpponentImage()
    datasets = oppi.return_datafiles()
    print(datasets)