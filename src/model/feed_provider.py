from dateutil import parser
from datetime import timezone, datetime
from abc import ABC, abstractmethod


class FeedProvider(ABC):
    def __init__(self, rss_url: str):
        self.rss_url = rss_url
        self.__feed = None

    @abstractmethod
    def get_fresh_feed(self):
        pass

    def __get_feed(self):
        if self.__feed:
            return self.__feed
        else:
            return self.get_fresh_feed()

    def get_feed_entries(self, start_date: datetime = None, end_date: datetime = None):
        feed = self.__get_feed()
        if start_date is None:
            start_date = datetime.min.replace(tzinfo=timezone.utc)
        if end_date is None:
            end_date = datetime.max.replace(tzinfo=timezone.utc)
        return [episode for episode in feed.entries if start_date < parser.parse(episode.published) < end_date]






