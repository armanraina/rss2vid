from src.model import feed_provider_factory
from src.model.request import Request
from src.model.response import Response
from src.model import episode_processor
from src.model.progress_updater import ProgressUpdater
from src.model.download_exception import DownloadException
from src.model.feed_exception import FeedException
from src.model.feed_provider import FeedProvider
from src.model.conversion_exception import ConversionException

class RequestProcessor:
    def __init__(self, progress_updater: ProgressUpdater):
        self.progress_updater: ProgressUpdater = progress_updater

    def process(self, request: Request) -> Response:
        feed_provider: FeedProvider = feed_provider_factory.get_feed_provider(request.rss_url)
        try:
            episodes = feed_provider.get_feed_entries(request.start_date)
            return self.__handle_episodes(episodes, request)
        except FeedException as e:
            return Response(0, 0, []).fail(str(e))

    def __handle_episodes(self, episodes, request: Request) -> Response:
        total_episodes: int = len(episodes)
        response: Response = Response(total_episodes, 0, [])
        for i, episode in enumerate(episodes):
            self.progress_updater.update_progress(i + 1, response.total_episodes)
            try:
                episode_processor.process(episode, request)
            except (DownloadException, ConversionException) as e:
                response.skip_episode(str(e))
        return response
