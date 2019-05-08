#use original NN (for expart)
from keras.models import Sequential
from keras.layers import Convolution2D, Dense

class TestNet():
    def __init__(self, params):
        self.wh = params['ml']['img_size_xy']


