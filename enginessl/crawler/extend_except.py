class QueryError(Exception):
    def err(self):
        print("[QueryError] An abnormality was found in the search query.")
        exit()

class HTTPError(Exception):
    def err(self):
        print("[HTTPError] Response result is incomplete.")
        exit()

class CrawlingError(Exception):
    def err(self):
        print("[CrawlingError] Failed to crawl.")
        exit()