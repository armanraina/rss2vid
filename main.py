from config_manager import get_config
from Request import Request
from Downloader import Downloader
from Converter import Converter
from RequestProcessor import RequestProcessor
from FeedProvider import FeedProvider
from EpisodeProcessor import EpisodeProcessor
from dateutil import parser

config = get_config()
rss_url = config['DEFAULT']['RSS_URL']
start_date = parser.parse(config['DEFAULT']['START_DATE'])
base_dir = config['DEFAULT']['BASE_DIR']
input_audio_ext = config['DEFAULT']['EXT_INPUT_AUDIO']
output_video_ext = config['DEFAULT']['EXT_OUTPUT_VIDEO']
image = config['DEFAULT']['IMAGE']
chunk_size = int(config['DEFAULT']['CHUNK_SIZE'])

request = Request(rss_url,
                  start_date,
                  base_dir,
                  input_audio_ext,
                  output_video_ext,
                  image,
                  chunk_size)
downloader = Downloader(request.chunk_size)
converter = Converter()
feed_provider = FeedProvider(request.rss_url)
episode_processor = EpisodeProcessor(converter, downloader)
request_processor = RequestProcessor(feed_provider, episode_processor)
request_processor.process(request)


