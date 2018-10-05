import os
import sys
from time import sleep
import requests
import bs4

class Kernel:

    def __init__(self):
        self.meta = self._metadata_config()
        self.params = self._read_yaml(str(self.meta[1]))
        print(self.params)

    def get_url(self, keyword):
        get_num = int(self.params['crawler']['target_num'])
        ua = self.params['crawler']['user_agent'] if self.params['crawler']['user_agent'] != None else ""
        mail = self.params['crawler']['mail'] if self.params['crawler']['mail'] != None else ""
        wait = self.params['crawler']['wait_sec'] if self.params['crawler']['wait_sec'] != None else 1.0
        self.fetcher = Fetcher(ua=ua, mail=mail, wait=wait, target_server=str(self.meta[0]))
        if keyword == "" or keyword == None or get_num == None or int(get_num) <= 0:
            print("[QueryError] An abnormality was found in the search query.")
            exit()
        access_iter, diff_num = int(get_num / 60.1), int(get_num % 60)
        # multiple_access_mode = True if access_iter != 0 else False
        html_datas = []
        for step in range(1,access_iter+2):
            keyword_query = 'p={}'.format(keyword)
            if step != 1:
                keyword_query += ' ' + str(step)
            num_query = 'n={}'.format(diff_num if step == access_iter+1 else 60)
            full_query = '?'+ keyword_query + '&' + num_query
            html_datas.append(self.fetcher.fetch(full_query))
        self.check_html(html_datas)
        all_img_urls = [self.scrape(page) for page in html_datas]


    def check_html(self, htmls):
        if None in htmls:
            print("[Caution] Response result is incomplete.\nThe number of acquisitions may be less than the specified number")

    def scrape(self, html):
        bs = bs4.BeautifulSoup(html, self.params['crawler']['for_expart']['parser'])
        onepage_img_tags = [a.img.get('src') for a in bs.find_all('a', attrs={'target': 'imagewin'}) if not a.img.get('src').endswith('.gif')]
        # print(onepage_img_tags)
        # print(len(onepage_img_tags))






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

    def __init__(self, ua, mail, wait, target_server):
        self.send_header = {
            'User-Agent': ua,
            'From': mail
        }
        self.wait = wait
        self.target_server = target_server

    def fetch(self, q):
        sleep(self.wait)
        send_url = self.target_server + q
        response = requests.get(send_url, headers=self.send_header)
        mimetype = response.headers['content-type']
        if mimetype.split(';')[0] != 'text/html':
            return None
        return response.text




if __name__ == '__main__':
    a = Kernel()
    a.get_url("suiseiseki")