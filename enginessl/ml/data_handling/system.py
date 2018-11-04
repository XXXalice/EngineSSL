from . import kernel

class DataHandling(kernel.OpponentImage):

    def __init__(self):
        print('Data processing execution.')
        self.oppo = kernel.OpponentImage()

    def get_builtup_data(self):
        return self.oppo.return_datafiles()

    def test_show(self, img_bin):
        self.oppo.test_show()

