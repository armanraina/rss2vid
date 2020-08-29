import configparser
from dateutil import parser
import os.path
from src.util import data_path
from src.constants import DEFAULT_DATE_STR
from src.model import request


class ArgumentCacheManager:

	def __init__(self, filename: str = 'config.ini'):
		self.filename = filename

	def initialize_cache(self, date_str):
		config = configparser.ConfigParser()

		config['DEFAULT']['RSS_URL'] = 'https://www.spreaker.com/show/4254204/episodes/feed'
		config['DEFAULT']['BASE_DIR'] = data_path('')
		config['DEFAULT']['EXT_INPUT_AUDIO'] = '.mp3'
		config['DEFAULT']['EXT_OUTPUT_VIDEO'] = '.mkv'
		config['DEFAULT']['IMAGE'] = os.path.join(config['DEFAULT']['BASE_DIR'], 'samples', 'mic.jpg')
		config['DEFAULT']['START_DATE'] = date_str
		config['DEFAULT']['CHUNK_SIZE'] = '1024'

		with open(data_path(self.filename), 'w') as configfile:
			config.write(configfile)

	def get_config(self):
		if not os.path.isfile(data_path(self.filename)):
			self.initialize_cache(DEFAULT_DATE_STR)
		config = configparser.ConfigParser()
		config.read(data_path(self.filename))
		return config

	def update_date(self, date):
		config = configparser.ConfigParser()
		config.read(data_path(self.filename))
		date = max(parser.parse(config['DEFAULT']['START_DATE']), date)
		config['DEFAULT']['START_DATE'] = str(date)
		with open(self.filename, 'w+') as configfile:
			config.write(configfile)

	def update_config(self, request: request):
		config = configparser.ConfigParser()

		config['DEFAULT']['RSS_URL'] = request.rss_url
		config['DEFAULT']['BASE_DIR'] = request.base_dir
		config['DEFAULT']['EXT_INPUT_AUDIO'] = request.input_audio_ext
		config['DEFAULT']['EXT_OUTPUT_VIDEO'] = request.output_video_ext
		config['DEFAULT']['IMAGE'] = request.image
		config['DEFAULT']['START_DATE'] = str(request.start_date)
		config['DEFAULT']['CHUNK_SIZE'] = str(request.chunk_size)

		with open(self.filename, 'w+') as configfile:
			config.write(configfile)
