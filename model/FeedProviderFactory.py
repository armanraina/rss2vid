from model.FeedProvider import FeedProvider
from model.XMLFeedProvider import XMLFeedProvider
from model.HTMLFeedProvider import HTMLFeedProvider
import requests


class FeedProviderFactory:
    def __init__(self):
        pass

    def get_feed_provider(self, rss_url: str) -> FeedProvider:
        response = requests.get(rss_url)
        content_type = response
        if 'xml' in content_type:
            return XMLFeedProvider(rss_url)
        else:
            return HTMLFeedProvider(rss_url)





