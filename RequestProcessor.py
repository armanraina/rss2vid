from FeedProvider import FeedProvider
from Request import Request
from EpisodeProcessor import EpisodeProcessor
from dateutil import parser


class RequestProcessor:
    def __init__(self, feed_provider: FeedProvider, episode_processor: EpisodeProcessor):
        self.feed_provider = feed_provider
        self.episode_processor = episode_processor

    def process(self, request: Request):
        self.episode_processor.set_request(request)
        for episode in self.feed_provider.yield_feed_entries(request.start_date):
            self.episode_processor.process(episode)






