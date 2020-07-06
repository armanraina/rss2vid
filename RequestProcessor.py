from FeedProvider import FeedProvider
from Request import Request
from EpisodeProcessor import EpisodeProcessor
from ProgressUpdater import ProgressUpdater


class RequestProcessor:
    def __init__(self, feed_provider: FeedProvider,
                 episode_processor: EpisodeProcessor,
                 progress_updater: ProgressUpdater):
        self.feed_provider = feed_provider
        self.episode_processor = episode_processor
        self.progress_updater = progress_updater

    def process(self, request: Request):
        self.episode_processor.set_request(request)
        total_episodes: int = self.feed_provider.get_number_of_entries(request.start_date)
        for i, episode in enumerate(self.feed_provider.yield_feed_entries(request.start_date)):
            self.episode_processor.process(episode)
            self.progress_updater.update_progress(i+1, total_episodes)






