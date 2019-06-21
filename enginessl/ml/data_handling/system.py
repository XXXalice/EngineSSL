from . import kernel


class DataHandling(kernel.OpponentImage, kernel.Kernel):

    def __init__(self, target_label, image_tanks=[]):
        print('Data processing execution.')
        # self.oppo = kernel.OpponentImage(image_tanks)
        self.data_handling = kernel.Kernel(image_tanks)
        # print('labels :{}'.format(self.oppo.labels))

    def get_builtup_data_not_include_noise(self):
        """
        :return: tuple (self.x_train, self.x_test, self.y_train, self.y_test)
        """
        return self.data_handling.data_preprocess()

    def oppo_kernel(self, image_tanks=[]):
        print('Noise data processing execution.')
        self.oppo = kernel.OpponentImage(image_tanks)


    def get_builtup_data(self):
        """
        :return: tuple (self.x_train, self.x_test, self.y_train, self.y_test)
        """
        return self.oppo.return_datafiles()

    def test_show(self, img_bin):
        self.oppo.test_show(img_bin)