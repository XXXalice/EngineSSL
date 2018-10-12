from . import kernel
from .extend_except import CrawlingError

class Clawler():

    def __init__(self):
        self.c = kernel.Kernel()
        self.urls = None

    def crawl(self, keyword, num):
        self.urls = self.c.get_url(keyword, num)

    def save_img(self):
        if not self.urls:
            self.c.save_img(self.urls)
        else:
            raise CrawlingError