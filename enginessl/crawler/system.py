from kernel import Kernel
from extend_except import CrawlingError

class Clawler(Kernel):

    def __init__(self):
        self.c = Kernel()
        self.urls = None

    def crawl(self, keyword, num):
        self.urls = self.c.get_url(keyword, num)

    def save_img(self):
        if not self.urls:
            self.c.save_img(self.urls)
        else:
            raise CrawlingError