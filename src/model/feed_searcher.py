import requests
from src.model.feed_exception import FeedException


class FeedSearcher:
    SERVICE_URL = "https://feedsearch.dev/api/v1/search"

    def __init__(self, **options):
        self.options = options

    def search(self, rss_url):
        params = {'url': rss_url}
        params.update(self.options)
        response = requests.get(self.SERVICE_URL, params=params)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise FeedException(f'{self.__class__.__name__}: Wrong response code : {response.status_code}')
