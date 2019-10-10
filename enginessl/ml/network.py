#use original NN (for expart)
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout

class TestNet():
    def __init__(self, params):
        self.hw = params['ml']['img_size_xy']
        self.channel = 1 if params['ml']['grayscale'] == True else 3


    def generate_model(self, num_classes):
        self.x_train, self.x_test, self.y_train, self.y_test = datas
        self.num_classes = num_classes
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same', activation='relu',input_shape=(self.hw, self.hw, self.channel)))
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

    def say(self, message):
        print(message)