import requests


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
            print(response.status_code)