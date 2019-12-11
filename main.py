from config_manager import get_config
from Request import Request
from Downloader import Downloader
from Converter import Converter
from RequestProcessor import RequestProcessor
from FeedProvider import FeedProvider
from EpisodeProcessor import EpisodeProcessor

config = get_config()
request = Request(config)
downloader = Downloader(request.chunk_size)
converter = Converter()
feed_provider = FeedProvider(request.rss_url)
episode_processor = EpisodeProcessor(converter, downloader)
request_processor = RequestProcessor(feed_provider, episode_processor)
request_processor.process(request)


