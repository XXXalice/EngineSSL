from . import kernel
from . import extend_except as ex

class Clawler(kernel.Kernel):
    """
    クローラAPI
    一つのキーワードごとにインスタンス化する
    引数は配列で取る必要があり、[1]で取得枚数を上書きできる（デフォルトはparam.ymlに記載された枚数）
    """
    def __init__(self, arg):
        self.keyword = arg[0]
        self.num = int(arg[1]) if len(arg)!=1 else 0
        super().__init__()
        self.urls = None

    def crawl(self):
        self.urls = super().get_url(self.keyword, self.num)
        print(len(self.urls))

    def save_img(self, rtn_folpath=False):
        """
        フォルダを作成し画像を収集する
        :return: 作成したフォルダの絶対パス
        """
        if self.urls:
            super().save_img(self.urls)
            rtn = self.made_imgdir if rtn_folpath else None
            return rtn
        else:
            raise ex.CrawlingError