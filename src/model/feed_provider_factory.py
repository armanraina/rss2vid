from src.model.feed_provider import FeedProvider
from src.model.xml_feed_provider import XMLFeedProvider
from src.model.html_feed_provider import HTMLFeedProvider
import requests


def get_feed_provider(rss_url: str) -> FeedProvider:
    response = requests.get(rss_url)
    content_type = response.headers.get('content-type')
    if 'xml' in content_type:
        return XMLFeedProvider(rss_url)
    else:
        return HTMLFeedProvider(rss_url)





