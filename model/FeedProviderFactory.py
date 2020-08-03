from model.FeedProvider import FeedProvider
from model.XMLFeedProvider import XMLFeedProvider
from model.HTMLFeedProvider import HTMLFeedProvider
import requests


class FeedProviderFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_feed_provider(rss_url: str) -> FeedProvider:
        response = requests.get(rss_url)
        content_type = response.headers.get('content-type')
        if 'xml' in content_type:
            return XMLFeedProvider(rss_url)
        else:
            return HTMLFeedProvider(rss_url)





