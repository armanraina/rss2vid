import feedparser
from src.model.FeedProvider import FeedProvider
from src.model.FeedSearcher import FeedSearcher


class HTMLFeedProvider(FeedProvider):

    def get_fresh_feed(self):
        feed_searcher = FeedSearcher()
        feeds = feed_searcher.search(self.rss_url)
        podcast_url = feeds[0]['url']
        self.__feed = feedparser.parse(podcast_url)
        return self.__feed








