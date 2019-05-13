import os

import numpy as np
import keras
from PIL import Image
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import array_to_img

class Network():
    def __init__(self, params):
        print('easymode_test_ok')
        self.hw = params['ml']['img_size_xy']
    def mynet(self):
        model = Sequential()
        # model.add(Conv2D(32, (3, 3), padding='same', input_shape=(self.hw, self.hw, 1)))
        # model.add(Activation('relu'))
        # model.add(Conv2D(32, (3, 3), padding='same'))
        # model.add(Activation('relu'))
        # model.add(MaxPooling2D(pool_size=(2, 2)))
        # model.add(Dropout(0.25))
        # model.add(Flatten())
        # model.add(Dense(256))
        # model.add(Activation('relu'))
        # model.add(Dropout(0.25))
        # model.add(Dense(2))
        # model.add(Activation('softmax'))
        model.add(Conv2D(16, (3, 3), activation='relu', input_shape=(self.hw, self.hw, 1)))
        model.add(Conv2D(16, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2, activation='softmax'))

        return model

    def train(self, model, datas, data_check=True):

        x_train = [flat_img.reshape(100, 100, 1) for flat_img in datas[0]]
        x_test = [flat_img.reshape(100, 100, 1) for flat_img in datas[1]]
        x_train = np.asarray(x_train).astype('float32')
        x_test = np.asarray(x_test).astype('float32')
        y_train, y_test = datas[-2:]

        if data_check == True:
            self.datas = (x_train, x_test, y_train, y_test)
            self._data_check()

        print('x_train:', len(x_train), x_train.shape)
        print('x_test:', len(x_test), x_test.shape)
        print('y_train:', len(y_train), y_train.shape)
        print('y_test:', len(y_test), y_test.shape)



        # for layer in model.layers:
        #     layer.trainable = True
        model.compile(loss='categorical_crossentropy',
                      optimizer='SGD',
                      metrics=['accuracy'])
        model.fit(x_train,
                  y_train,
                  batch_size=5,
                  epochs=200,
                  validation_data=(x_test, y_test),
                  verbose=0
                  )
        os.makedirs('./models', exist_ok=True)
        model.save('./models/'+'easymode.h5')

    def _data_check(self):
        x_train, x_test, y_train, y_test = self.datas
        flat_x = x_train[3]
        reshape_x = flat_x.reshape(100, 100, 1)
        flat_oppo_x = x_train[-1]
        reshape_oppo_x = flat_oppo_x.reshape(100, 100, 1)
        check_arr = [flat_x, reshape_x, flat_oppo_x, reshape_oppo_x]

        print('-'*30)
        print('start data check.','\n'*2)
        print(type(y_train))
        print(y_train)
        for check_img in check_arr:
            print(type(check_img))
            print(check_img.shape)

        savedir = './test/check_imgs/'
        os.makedirs(savedir, exist_ok=True)
        for idx, check_img in enumerate(check_arr):
            try:
                img = array_to_img(check_img)
                img.save(savedir + 'test_img{}.jpg'.format(idx))
                print('saved img.')
            except Exception as e:
                print('cant read img.', e)
                continue
        print('\n'*2, 'finish data check.')
        print('-' * 30)