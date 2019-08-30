from . import kernel
from . import extend_except as ex
import inspect
import os
import shutil

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

    def crawl(self, multiple=1):
        self.urls = super().get_url(self.keyword, num=self.num, multiple=multiple)
        print(len(self.urls))

    def save_img(self, rtn_folpath=False):
        """
        フォルダを作成し画像を収集する
        :return: 作成したフォルダの相対パス
        """
        if self.urls:
            super().save_img(self.urls)
            rtn = self.made_imgdir if rtn_folpath else None
            return rtn
        else:
            raise ex.CrawlingError

    def delete_datas_dir(self):
        """
        data/img配下を全削除
        :return: なし
        """
        data_path = os.path.join('/'.join(inspect.stack()[0][1].split('/')[:-2]), 'data', 'img')
        if os.path.exists(data_path):
            shutil.rmtree(data_path)
            os.makedirs(path=data_path, exist_ok=True)
            print('init data stacks.')
