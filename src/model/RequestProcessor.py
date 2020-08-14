from src.model import FeedProviderFactory
from src.model import Request
from src.model import EpisodeProcessor
from src.model import ProgressUpdater
from src.model import DownloadException


class RequestProcessor:
    def __init__(self, feed_provider_factory: FeedProviderFactory,
                 episode_processor: EpisodeProcessor,
                 progress_updater: ProgressUpdater):
        self.feed_provider_factory = feed_provider_factory
        self.episode_processor = episode_processor
        self.progress_updater = progress_updater

    def process(self, request: Request):
        print(repr(request))
        feed_provider = self.feed_provider_factory.get_feed_provider(request.rss_url)
        print(feed_provider)
        self.episode_processor.set_request(request)
        total_episodes: int = feed_provider.get_number_of_entries(request.start_date)
        for i, episode in enumerate(feed_provider.yield_feed_entries(request.start_date)):
            self.progress_updater.update_progress(i+1, total_episodes)
            try:
                self.episode_processor.process(episode)
            except DownloadException as e:
                continue






