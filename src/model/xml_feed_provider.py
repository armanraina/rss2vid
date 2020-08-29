from src.model.feed_provider import FeedProvider
import feedparser


class XMLFeedProvider(FeedProvider):

    def get_fresh_feed(self):
        self.__feed = feedparser.parse(self.rss_url)
        return self.__feed
