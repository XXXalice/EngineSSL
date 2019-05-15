import os
import sys
from time import sleep
import requests
import bs4


class Kernel:
    def __init__(self):
        try:
            self.meta = self.metadata_config()
            self.params = self.read_yaml(str(self.meta[1]))
        except:
            sys.stderr.write("[InstanceError] Metadata is incomplete.\n")
            exit()

    def get_url(self, keyword, num):
        self.mk_dir(keyword)
        get_num = int(self.params['crawler']['target_num']) if num != '' else num
        ua = self.params['crawler']['user_agent'] if self.params['crawler']['user_agent'] != None else ""
        mail = self.params['crawler']['mail'] if self.params['crawler']['mail'] != None else ""
        wait = self.params['crawler']['wait_sec'] if self.params['crawler']['wait_sec'] != None else 1.0
        self.fetcher = Fetcher(ua=ua, mail=mail, wait=wait, target_server=str(self.meta[0]))
        if keyword == "" or keyword == None or get_num == None or int(get_num) <= 0:
            print("[QueryError] An abnormality was found in the search query..")
            exit()
        access_iter, diff_num = int(get_num / 60.1), int(get_num % 60)
        # multiple_access_mode = True if access_iter != 0 else False
        html_datas = []
        for step in range(1,access_iter+2):
            keyword_query = 'p={}'.format(keyword)
            if step != 1:
                keyword_query += (' ' + str(step))
            if get_num != 60:
                num_query = 'n={}'.format(diff_num if step == access_iter+1 else 60)
            else:
                num_query = 'n={}'.format(60)
            full_query = '?'+ keyword_query + '&' + num_query
            html_datas.append(self.fetcher.fetch_html(full_query))
        self.check_html(html_datas)
        all_img_urls = [url for onepage_urls in [self.scrape(page) for page in html_datas] for url in onepage_urls]
        return all_img_urls

    def mk_dir(self, keyword):
        from datetime import datetime
        datapath = self.meta[2]
        if not os.path.exists(datapath):
            os.makedirs(datapath)
        now = datetime.now()
        current_time = '_{y}_{m}_{d}_{h}_{mi}_{s}'.format(y=str(now.year), m=str(now.month), d=str(now.day),
                                                      h=str(now.hour), mi=str(now.minute), s=str(now.second))
        dirname = os.path.join(datapath, keyword+current_time)
        try:
            os.mkdir(dirname)
            self.made_imgdir = dirname
            return
        except:
            sys.stderr.write("[MkdirError] There is a deficiency in folder construction.")
            exit()

    def check_html(self, htmls):
        if None in htmls:
            print("[Caution] Response result is incomplete.\nThe number of acquisitions may be less than the specified number")

    def scrape(self, html):
        bs = bs4.BeautifulSoup(html, self.params['crawler']['for_expart']['parser'])
        onepage_img_tags = [a.img.get('src') for a in bs.find_all('a', attrs={'target': 'imagewin'}) if not a.img.get('src').endswith('.gif')]
        return onepage_img_tags

    def save_img(self, urls):
        success_count = 0
        ext = self.params['crawler']['ext']
        for url in urls:
            img = self.fetcher.fetch_img(url)
            if img != None:
                success_count += 1
            else:
                print('download faild.')
            img_name = '{:03}.{}'.format(success_count, ext)
            with open(os.path.join(self.made_imgdir + '/' +img_name), "wb") as save:
                print('downloaded from :{}'.format(url))
                save.write(img)

    def metadata_config(self):
        with open('crawler/.crawler_metadata', 'r') as f:
            config = f.readlines()
        return [conf.strip() for conf in config]

    def read_yaml(self, uri):
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
        self.timeout = 3

    def fetch_html(self, q):
        sleep(self.wait)
        send_url = self.target_server + q
        response = requests.get(send_url, headers=self.send_header, timeout=self.timeout)
        if response.status_code != 200:
            err = Exception("http status:{}".format(response.status_code))
            raise err
        mimetype = response.headers['content-type']
        if mimetype.split(';')[0] != 'text/html':
            return None
        return response.text

    def fetch_img(self, url):
        sleep(self.wait)
        response = requests.get(url, headers=self.send_header, timeout=self.timeout)
        if response.status_code != 200:
            err = Exception("http status:{}".format(response.status_code))
            raise err
        mimetype = response.headers['content-type']
        if 'image' not in mimetype:
            return None
        return response.content



# kernel test
# if __name__ == '__main__':
#     a = Kernel()
#     urls = a.get_url("岡尚大")
#     a.save_img(urls=urls)