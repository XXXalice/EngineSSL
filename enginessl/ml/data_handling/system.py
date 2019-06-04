from . import kernel


class DataHandling(kernel.OpponentImage):

    def __init__(self, image_tanks=[]):
        print('Data processing execution.')
        self.oppo = kernel.OpponentImage(image_tanks)
        print('labels :{}'.format(self.labels))

    def get_builtup_data(self):
        """
        :return: tuple (self.x_train, self.x_test, self.y_train, self.y_test)
        """
        return self.oppo.return_datafiles()

    def test_show(self, img_bin):
        self.oppo.test_show(img_bin)