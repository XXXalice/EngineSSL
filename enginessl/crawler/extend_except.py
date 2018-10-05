class QueryError(Exception):
    print("[QueryError] An abnormality was found in the search query.")
    exit()

class HTTPError(Exception):
    print("[HTTPError] Response result is incomplete.")
    exit()