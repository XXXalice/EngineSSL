import json
from lxml.etree import parse
import os
import urllib.request
import urllib.parse
import pprint
import base64

class UseApis:
    def __init__(self, base="", server_name=""):
        self.base = base
        self.server = server_name

    def load_secrets(self, sec_path):
        try:
            with open(sec_path, mode="r", encoding="utf-8") as sec:
                elems = [elem.rstrip(os.linesep) for elem in sec.readlines()]
            self.CLIENT_ID = elems[0]
            self.CLIENT_SEC = elems[1]
        except Exception as e:
            self.CLIENT_ID = None
            self.CLIENT_SEC = None
            print(e)

    def construct_url(self, **query):
        if self.base[-1:] != "?":
            self.base += "?"
        query_strings = []
        for param, value in query.items():
            query_strings.append("{}={}".format(str(param), str(value)))
        self.base += "&".join(query_strings)

    def url_request(self):
        body = None
        print("send request...")
        try:
            req = urllib.request.Request(self.base)
            with urllib.request.urlopen(req) as resp:
                body = resp.read()
        except Exception as e:
            print(e)
        finally:
            print("operation has ended.")
        return body

    def xml2json(self, xml):
        tree = parse(xml)
        roots = tree.getroot()
        json_body = json.dumps(roots, indent=2)
        return json_body


class YahooPhrase(UseApis):
    def __init__(self):
        base_url = "https://jlp.yahooapis.jp/KeyphraseService/V1/extract"
        sec_path = "./YAHOO.sec"
        super().__init__(base=base_url, server_name="keypharase")
        self.load_secrets(sec_path=sec_path)

    def execute(self, *q, flexible_mode=True):
        if flexible_mode:
            q = q[0]
            queries = q.split(" ")
            sentence = queries[0]
        else:
            sentence = q[0]
        sentence = urllib.parse.quote(sentence)
        self.construct_url(appid=self.CLIENT_ID, sentence=sentence, output="json")
        resp = self.url_request()
        return resp

if __name__ == '__main__':
    pharase = YahooPhrase()
    sentence = input("いんぷーっと！：")
    json = pharase.execute(sentence)
    pprint.pprint(json)
