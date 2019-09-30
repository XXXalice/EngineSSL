from . import kernel


class DataHandling(kernel.OpponentImage ,kernel.Kernel):

    def __init__(self, target_label, image_tanks=[]):
        print('Data processing execution.')
        # self.oppo = kernel.OpponentImage(image_tanks)
        self.data_handling = kernel.Kernel(image_tanks)
        # print('labels :{}'.format(self.oppo.labels))

    def get_builtup_data(self,targets=[], not_targets=[], flatten=False, color_mode='grayscale'):
        """
        :return: tuple (self.x_train, self.x_test, self.y_train, self.y_test)
        x shape: (-1, hw, hw, channel)
        """
        return self.data_handling.data_preprocess(targets=targets, not_targets=not_targets, flatten=flatten, color_mode=color_mode)

    def read_dirs(self, datas_dir, target_label):
        """
        :return: tuple (target, not_target)
        """
        target_dir, not_target_dir = self.get_img_dir(target_label=target_label, split_tag=True)
        return target_dir, not_target_dir
        return self.read_datas_dir(datas_dir=datas_dir, target_label=target_label)

    def oppo_kernel(self, target_dir, image_tanks):
        print('Noise data processing execution.')
        self.oppo = kernel.OpponentImage(target_dir=target_dir ,image_tanks=image_tanks, params=self.data_handling.params)
        return self.oppo

    def make_noise(self):
        print('Making noise data.')
        self.oppo.make_noise()

    def get_builtup_data_include_noise(self):
        """
        :return: tuple (self.x_train, self.x_test, self.y_train, self.y_test)
        """
        return self.oppo.return_datafiles()

    def test_show(self, img_bin):
        self.oppo.test_show(img_bin)