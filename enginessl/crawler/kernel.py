import os
import sys

class Kernel:

    def __init__(self):
        self.meta = self._metadata_config()
        self.params = self._read_yaml(str(self.meta[1]))
        print(self.params)

    def get_url(self, keyword):
        import requests
        get_num = int(self.params['crawler']['target_num'])
        if keyword == "" or keyword == None or get_num == None or int(get_num) <= 0:
            print("[QueryError] An abnormality was found in the search query.")
            exit()
        access_iter, diff_num = int(get_num / 60), int(get_num % 60)
        for step in range(2,access_iter+2):
            keyword_query, num_query = 'p={}'.format(keyword), 'n={}'.format()

    def crawling(self, mode, q):
        pass

    def scrape(self, body):
        pass

    def _metadata_config(self):
        with open('.crawler_metadata', 'r') as f:
            config = f.readlines()
        return [conf.strip() for conf in config]

    def _read_yaml(self, uri):
        import yaml
        try:
            with open(uri, 'r') as d:
                param_dict = yaml.load(d)
        except Exception as err:
            sys.stdout.write(str(err))
            return
        return param_dict



if __name__ == '__main__':
    a = Kernel()
    a.get_url("a")