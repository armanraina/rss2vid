from model.FeedProvider import FeedProvider
import feedparser
from abc import ABC, abstractmethod


class XMLFeedProvider(FeedProvider):

    def get_fresh_feed(self):
        self.__feed = feedparser.parse(self.rss_url)
        return self.__feed
