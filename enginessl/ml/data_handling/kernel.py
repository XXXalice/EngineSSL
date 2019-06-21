import numpy as np
import sys
import os
import gc
from keras.preprocessing.image import load_img, img_to_array, array_to_img, save_img , ImageDataGenerator
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
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

    def __init__(self, image_tanks=[]):
        self.exec_path = os.path.dirname(os.path.abspath(__file__))
        base = 'enginessl'
        img_dir = 'data/img'
        datas_dir = get_path_with_glob(self.exec_path, base, img_dir)
        if '.DS_Store' in datas_dir:
            datas_dir.remove('.DS_Store')
        if len(image_tanks) >= 1:
            """ラベル2が複数存在する場合"""
            self.datas_wrapper = []
            target_dir = []
            for dir_name in datas_dir:
                if dir_name in image_tanks:
                    target_dir.append(dir_name)
            """ターゲットデータディレクトリ更新"""
            datas_dir = target_dir
        else:
            self.datas_wrapper = None

        self.labels = list(map(lambda label: label.split('_')[0], datas_dir))
        self.params = self.read_yaml(get_path_with_glob(self.exec_path, base, 'param.yml'))
        # self.datas = get_path_with_glob(exec_path, base, '.+datas_dir[0] + '/*.{}'.format(self.params['crawler']['ext']))
        self.img_dir_abspath = []
        for idx, dir_name in enumerate(datas_dir):
            print('dir:', dir_name)
            self.img_dir_abspath.append(os.path.join(self.exec_path.split(base)[0], base, img_dir, dir_name))
            if idx == 0:
                self.datas = [self.img_dir_abspath[idx] + '/' + img_name for img_name in get_path_with_glob(self.exec_path, base, dir_name) if str(img_name) != 'fuzzies']
                self.datas.sort()
            else:
                self.oppo_datas = [self.img_dir_abspath[idx] + '/' + img_name for img_name in get_path_with_glob(self.exec_path, base, dir_name) if str(img_name) != 'fuzzies']
                self.oppo_datas.sort()
            print('finish. {}'.format(dir_name))


    def data_split(self, datas, validation=False):
        """
        データ分割
        :param datas: 分割対象のリスト
        :param validation:
        :return: 分割後のタプル
        """
        try:
            test_num = int(len(datas) * self.params['ml']['test_data_rate'])
            train_num = len(datas) - test_num
            self.x_train_raw = datas[:train_num]
            self.x_test_raw = datas[-test_num:]
        except Exception as err:
            sys.stdout.write(str(err))
        else:
            print('splited datas. test:{test}  train:{train}'.format(test=len(self.x_train_raw), train=len(self.x_test_raw)))
            return (self.x_train_raw, self.x_test_raw)

    def data_preprocess_basic(self, splited_datas, gray=True, size=(100,100), label=0, precision=np.float32):
        """
        単一語句のデータ前処理
        :param splited_datas:
        :param gray:
        :param size:
        :param label:
        :param precision:
        :return:
        """
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        size = [self.params['ml']['img_size_xy']]*2 if not self.params['ml']['img_size_xy'] == None else size
        for tr_or_ts, valid in enumerate([splited_datas[0], splited_datas[1]]):
            for img_path in valid:
                try:
                    img = load_img(img_path, color_mode='grayscale', target_size=size)
                    img_bin = img_to_array(img)
                    # data_container[label].append(img_bin)
                    if tr_or_ts == 0:
                        self.x_train.append(img_bin)
                        self.y_train.append(label)
                        print('encoded img for train.[{}]'.format(img_path))
                    elif tr_or_ts == 1:
                        self.x_test.append(img_bin)
                        self.y_test.append(label)
                        print('encoded img for test.[{}]'.format(img_path))
                except:
                    print('cant preprocessed image.[{}]'.format(img_path))
                    continue
                else:
                    pass
            # self.x_train = list(map(lambda img_bin: np.float16(img_bin)/255, self.x_train))
            # self.x_test = list(map(lambda img_bin: np.float16(img_bin) / 255, self.x_test))
            self.x_train = list(map(lambda img_bin: np.ravel(precision(img_bin) / 255.0), self.x_train))
            self.x_test = list(map(lambda img_bin: np.ravel(precision(img_bin) / 255.0), self.x_test))
        print('data shape {}'.format(self.x_train[0].shape))
        print('train {}  test {}'.format(len(self.x_train), len(self.x_test)))

    def data_preprocess(self, flatten=True, color_mode='grayscale'):
        """
        2つ以上の単語が与えられた際の前処理
        画像のフルパスを受け取る
        """
        def norm(x):
            try:
                x = np.asarray(x)
            except:
                pass
            finally:
                x = x.astype('float32')
                x /= 255.0
                return x

        targets = self.datas
        not_targets = self.oppo_datas
        x = []
        y = []
        size = [self.params['ml']['img_size_xy']] * 2 if not self.params['ml']['img_size_xy'] == None else (100, 100)
        for idx, datas in enumerate([targets, not_targets]):
            for data in datas:
                img_bin = img_to_array(load_img(data, color_mode=color_mode, target_size=size))
                x.append(img_bin)
                y.append(idx)
        y = np.asarray(y)
        if flatten:
            x = [np.ravel(img_bin) for img_bin in x]
        x = norm(x)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=self.params['ml']['test_data_rate'], shuffle=False)
        return (self.x_train, self.x_test, self.y_train, self.y_test)


    def read_yaml(self, uri):
        import yaml
        try:
            with open(uri, 'r') as d:
                param_dict = yaml.load(d)
        except Exception as err:
            sys.stdout.write(str(err))
            return
        return param_dict


class OpponentImage(Kernel):
    """
    対立的画像の生成クラス
    データ前処理用クラスを継承している
    """
    def __init__(self, image_tanks):
        self.multiple_models = False if len(image_tanks) <= 1 else True
        train, test = [], []
        if self.multiple_models:
            Kernel.__init__(self, image_tanks)
            for d in (self.datas, self.oppo_datas):
                splited = self.data_split(d)
                train.append(splited[0])
                test.append(splited[1])
        else:
            Kernel.__init__(self)
            splited = self.data_split(self.datas)
            train.append(splited[0])
            test.append(splited[1])
        train = sum(train, [])
        test = sum(test, [])
        self.data_preprocess_basic(splited_datas=(train, test))
        self.__gc_vals(train, test)
        self.ancestors = [self.x_train, self.x_test]
        self.ancestors_label = [self.y_train, self.y_test]
        self.decay = self.params['oppoimg']['decay']
        self.mode = self.params['oppoimg']['mode']
        # self.exe_oppo()
        self.make_fuzzyimg(decay=self.decay, effect=self.mode)

    def exe_oppo(self):
        self.make_fuzzyimg(decay=self.decay, effect=self.mode)
        if hasattr(self, 'fuzzies_save_dir'):
            oppoimgs = [self.fuzzies_save_dir + '/' + oppoimg for oppoimg in os.listdir(self.fuzzies_save_dir)]
            oppoimgs.sort()
            return oppoimgs
        else:
            print('Error in OpponentImg.')
            exit()

    def make_fuzzyimg(self, decay, effect, img_save=True):
        from . import effect_func as ef

        e_dict = {
            's_random': lambda x: ef.simple_random(x),
            'swap': lambda x: ef.swap(x),
            'as_random': lambda  x: ef.ancestral_scale_random(x),
            'as_randomv2': lambda x: ef.ancestral_scale_random_v2(x)
        }

        success_num = 0
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
                        self.y_train.append(1)
                    elif i == 1:
                        self.x_test.append(effected_bin)
                        self.y_test.append(1)
                except:
                    print('cant generate fuzzyimg.')
                    continue
                else:
                    success_num += 1
                    if img_save == True:
                        self.save_fuzzyimg(np_img=effected_bin, num=success_num)
                    print('generated fuzzyimg. num:{}'.format(success_num))
        print('fuzzy mode {}'.format(effect))
        # self.test_show(self.ancestors[0][150])

    def save_fuzzyimg(self, np_img, num):
        datas_dir_name = get_path_with_glob(self.exec_path, 'enginessl', 'data/img')[0]
        absdatas_dir = get_path_with_glob(self.exec_path, 'enginessl', 'data', abs=True)
        self.fuzzies_save_dir = os.path.join(absdatas_dir[0], datas_dir_name, 'fuzzies')
        if not os.path.exists(self.fuzzies_save_dir):
            os.mkdir(self.fuzzies_save_dir)
        ex_img = array_to_img(np_img.reshape(100,100,1))
        ex_img.save(os.path.join(self.fuzzies_save_dir, '{0:03d}.png'.format(num)))

    def anal_ances(self):
        pass

    def return_datafiles(self):
        self.y_train = to_categorical(self.y_train, num_classes=2)
        self.y_test = to_categorical(self.y_test, num_classes=2)
        return (self.x_train, self.x_test, self.y_train, self.y_test)

    def test_show(self, np_img):
        import matplotlib.pyplot as plt
        ex_img = array_to_img(np_img.reshape(100,100,1))
        ex_img.save('test.png')

    def __gc_vals(self, *objs):
        for rm_ival in objs:
            try:
                del rm_ival
            except:
                continue
        gc.collect()


# # kernel test
# if __name__ == '__main__':
#     k = Kernel()
#     k.data_split()
#     k.data_preprocess_basic()
#     oppi = OpponentImage()
#     datasets = oppi.return_datafiles()