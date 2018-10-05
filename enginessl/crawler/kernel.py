import os
import sys
import requests

class Kernel:

    def __init__(self):
        self.meta = self._metadata_config()
        self.params = self._read_yaml(str(self.meta[1]))
        print(self.params)

    def get_url(self, keyword):
        get_num = int(self.params['crawler']['target_num'])
        ua = self.params['crawler']['user_agent'] if self.params['crawler']['user_agent'] != None else ""
        self.fetcher = Fetcher(ua)
        if keyword == "" or keyword == None or get_num == None or int(get_num) <= 0:
            print("[QueryError] An abnormality was found in the search query.")
            exit()
        access_iter, diff_num = int(get_num / 60.1), int(get_num % 60)
        # multiple_access_mode = True if access_iter != 0 else False
        urls = []
        for step in range(1,access_iter+2):
            keyword_query = 'p={}'.format(keyword)
            if step != 1:
                keyword_query += str(step)
            num_query = 'n={}'.format(diff_num if step == access_iter+1 else 60)
            full_query = '?'+ keyword_query + '&' + num_query
            print(full_query)


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


class Fetcher:

    def __init__(self, ua):
        self.send_header = {
            'User-Agent': ua
        }


if __name__ == '__main__':
    a = Kernel()
    a.get_url("a")