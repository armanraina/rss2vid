import configparser
from dateutil import parser
import os.path


class ArgumentCacheManager:

	def __init__(self, directory: str, filename: str = 'config.ini'):
		self.directory = directory
		self.filename = filename

	def initialize_cache(self, date_str):
		config = configparser.ConfigParser()

		config['DEFAULT']['RSS_URL'] = 'citr.ca/radio/democracy-watch/'
		config['DEFAULT']['BASE_DIR'] = os.path.join(self.directory, 'samples')
		config['DEFAULT']['EXT_INPUT_AUDIO'] = '.mp3'
		config['DEFAULT']['EXT_OUTPUT_VIDEO'] = '.mkv'
		config['DEFAULT']['IMAGE'] = os.path.join(config['DEFAULT']['BASE_DIR'], 'mic.jpg')
		config['DEFAULT']['START_DATE'] = date_str
		config['DEFAULT']['CHUNK_SIZE'] = '1024'

		with open(os.path.join(self.directory, self.filename), 'w') as configfile:
			config.write(configfile)

	def get_config(self):
		config = configparser.ConfigParser()
		path = os.path.join(self.directory, self.filename)
		print(path)
		config.read(path)
		return config

	def update_date(self, date):
		config = configparser.ConfigParser()
		config.read(os.path.join(self.directory, self.filename))
		date = max(parser.parse(config['DEFAULT']['START_DATE']), date)
		config['DEFAULT']['START_DATE'] = str(date)
		with open(self.filename, 'w+') as configfile:
			config.write(configfile)

