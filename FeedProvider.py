import feedparser
from feedsearch_crawler import search
from dateutil import parser
from datetime import timezone, datetime


class FeedProvider:
    def __init__(self, rss_url: str):
        self.rss_url = rss_url

    def __get_feed(self):
        feeds = search(self.rss_url)
        podcast_url = feeds[0].url.human_repr()
        feed = feedparser.parse(podcast_url)
        return feed

    def yield_feed_entries(self, start_date: datetime = None, end_date: datetime = None):
        feed = self.__get_feed()
        if start_date is None:
            start_date = datetime.min.replace(tzinfo=timezone.utc)
        if end_date is None:
            end_date = datetime.max.replace(tzinfo=timezone.utc)
        yield from (episode for episode in feed.entries if start_date < parser.parse(episode.published) < end_date)


