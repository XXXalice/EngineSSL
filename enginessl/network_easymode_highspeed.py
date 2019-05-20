import os
import sys
import glob
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import img_to_array, load_img
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

class NetworkHighspeed():
    def __init__(self, params):
        self.dsstore = '.DS_Store'
        self.hw = params['ml']['img_size_xy'] #pixel
        self.color = params['ml']['grayscale'] #boolean
        self.t_rate = params['ml']['test_data_rate'] #float
        target_dir_name = os.listdir('./data/img')
        if '.DS_Store' in target_dir_name:
            target_dir_name.remove('.DS_Store')
        self.target_data_dir = './data/img/' + target_dir_name[0]
        self.num_classes = 2
        self.model_ext = params['ml']['savemodel_ext']

    def correct_datas(self):
        x = []
        y = []
        fuzzies_data_dir = self.target_data_dir + '/fuzzies'
        color = 'grayscale' if self.color else 'RGB'
        for index, data_dir in enumerate([self.target_data_dir, fuzzies_data_dir]):
            datas = glob.glob(data_dir + '/*.png')
            for data in datas:
                img = load_img(data, color_mode='grayscale', target_size=(self.hw, self.hw))
                img_array = img_to_array(img)
                x.append(img_array)
                y.append(index)
        x = np.asarray(x).astype('float32')
        x = x / 255
        y = to_categorical(np.asarray(y), self.num_classes)
        preprocessing_datas = self.__split_datas(x, y)
        return preprocessing_datas

    def __split_datas(self, x, y):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=self.t_rate)
        return (x_train, x_test, y_train, y_test)

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(16, (3, 3), activation='relu', input_shape=(self.hw, self.hw, 1)))
        model.add(Conv2D(16, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(self.num_classes, activation='softmax'))
        return model

    def train(self, model, preprocessing_datas, save_name):
        x_train, x_test, y_train, y_test = preprocessing_datas
        es_cb = EarlyStopping(monitor='val_loss', patience=0, verbose=0, mode='auto')
        model.compile(
            loss='categorical_crossentropy',
            optimizer='Adam',
            metrics=['accuracy']
        )
        self.hist = model.fit(
            x_train,
            y_train,
            batch_size=5,
            epochs=15,
            validation_data=(x_test, y_test),
            verbose=1,
            callbacks=[es_cb]
        )
        try:
            os.makedirs('./model', exist_ok=True)
            model.save('./model/' + save_name[0] + '.' + self.model_ext)
            made_model_name = save_name[0]+ '.' + self.model_ext
        except Exception as e:
            sys.stderr.write(str(e))
            sys.exit(0)
        finally:
            print('The operation has ended.')
            return made_model_name


    def __read_yaml(self, uri):
        import yaml
        try:
            with open(uri, 'r') as d:
                param_dict = yaml.load(d)
        except Exception as err:
            sys.stdout.write(str(err))
            return
        return param_dict