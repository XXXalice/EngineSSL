import os
import sys
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam


class TestNet():
    def __init__(self, params):
        self.params = params
        self.hw = self.params['ml']['img_size_xy']
        self.channel = 1 if self.params['ml']['grayscale'] == True else 3


    def generate_model(self, num_classes):
        self.num_classes = num_classes
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu',input_shape=(self.hw, self.hw, self.channel)))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(rate=0.25))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(Dropout(rate=0.25))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(rate=0.25))
        model.add(Dense(self.num_classes, activation='softmax'))
        return model

    def train(self, name, model, datas, es=True, optimizer=Adam()):
        x_train, y_train, x_test, y_test = datas
        if es:
            es_cb = EarlyStopping(monitor='val_loss', patience=3, verbose=0, mode='auto')

        model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy']
        )
        self.hist = model.fit(
            x_train,
            y_train,
            batch_size=5,
            epochs=30,
            verbose=1,
            validation_data=(x_test, y_test),
            callbacks=[es_cb] if es else None
        )
        os.makedirs('./model', exist_ok=True)
        model_name = name + self.params['ml']['savemodel_ext']
        model.save(os.path.join('model', model_name))
        print('the operation has ended.')
        return model_name


    def __say(self, message):
        print(message)