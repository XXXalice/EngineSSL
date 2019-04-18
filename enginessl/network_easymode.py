import os

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

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
        model.add(Dense(256, activation='relu'))
        model.add(Dense(2, activation='softmax'))

        return model

    def train(self, model, datas):
        x_train = np.array([flat_img.reshape(100, 100, -1) for flat_img in datas[0]])
        x_test = np.array([flat_img.reshape(100, 100, -1) for flat_img in datas[1]])

        # y_train = keras.utils.to_categorical(datas[2], 2)
        # y_test = keras.utils.to_categorical(datas[3], 2)
        y_train, y_test = datas[-2:]

        print('x_train:', x_train.shape)
        print('x_test:', x_test.shape)
        print('y_train:', y_train.shape)
        print('y_test:', y_test.shape)



        for layer in model.layers:
            layer.trainable = True
        model.compile(loss='categorical_crossentropy',
                      optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])
        model.fit(x_train,
                  y_train,
                  batch_size=32,
                  epochs=15,
                  validation_data=(x_test, y_test),
                  verbose=1
                  )
        os.makedirs('./models', exist_ok=True)
        model.save('./models/'+'easymode.h5')