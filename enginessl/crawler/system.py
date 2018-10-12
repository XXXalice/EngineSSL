from . import kernel
from . import extend_except as ex

class Clawler(kernel.Kernel):

    def __init__(self, arg):
        self.keyword = arg[0]
        self.num = int(arg[1]) if len(arg)!=1 else 0
        super().__init__()
        self.urls = None

    def crawl(self):
        self.urls = super().get_url(self.keyword, self.num)
        print(len(self.urls))

    def save_img(self):
        if self.urls:
            super().save_img(self.urls)
        else:
            raise ex.CrawlingError