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
        model.add(Conv2D(16, (3, 3), activation='relu',input_shape=(self.hw, self.hw, self.channel)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(rate=0.25))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(Dropout(rate=0.25))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(rate=0.25))
        model.add(Dense(self.num_classes, activation='softmax'))
        return model

    def train(self, name, model, datas, es, optimizer=Adam()):
        x_train, y_train, x_test, y_test = datas
        if es != 'none':
            es_cb = EarlyStopping(monitor='val_loss', patience=7, verbose=1, mode='auto')
        else:
            print('Not use callback!')
            es_cb = None

        model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy']
        )
        if es_cb != None:
            self.hist = model.fit(
                x_train,
                y_train,
                batch_size=5,
                epochs=30,
                verbose=1,
                validation_data=(x_test, y_test),
                callbacks=[es_cb]
            )
        else:
            self.hist = model.fit(
                x_train,
                y_train,
                batch_size=5,
                epochs=30,
                verbose=1,
                validation_data=(x_test, y_test),
            )

        os.makedirs('./model', exist_ok=True)
        model_name = name + self.params['ml']['savemodel_ext']
        model.save(os.path.join('model', model_name))
        print('the operation has ended.')
        return model_name

    def draw_graph(self, model_name):
        """
        グラフ描画
        :return: 未定
        """
        import inspect
        import os
        import matplotlib
        matplotlib.use('Agg')
        here = "/".join(inspect.stack()[0][1].split("/")[:-2])
        data_dir = os.path.join(here, "data")
        data_graphs_dir = os.path.join(data_dir, "graphs")
        pred_app_dir = os.path.join(here, "pred_app")
        pred_app_graphs_dir = os.path.join(pred_app_dir, "graphs")
        os.makedirs(data_graphs_dir)
        os.makedirs(pred_app_graphs_dir)
        from matplotlib import pyplot as plt
        if hasattr(self, 'hist'):
            plt.subplot(1, 2, 1)
            plt.plot(self.hist.history['acc'], label='acc')
            plt.plot(self.hist.history['val_acc'], linestyle='-', label='val_acc')
            plt.title('acc')
            plt.legend()
            plt.subplot(1, 2, 2)
            plt.plot(self.hist.history['loss'], label='loss')
            plt.plot(self.hist.history['val_loss'], linestyle='-', label='val_loss')
            plt.title('loss')
            plt.legend()
            plt.savefig(os.path.join(data_graphs_dir, "{}.png".format(model_name)))
            plt.savefig(os.path.join(pred_app_graphs_dir, "{}.png".format(model_name)))
    def __say(self, message):
        print(message)