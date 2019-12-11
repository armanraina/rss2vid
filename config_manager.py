import configparser
from datetime import timezone, datetime
from dateutil import parser


def initialize_config(date_str):
	config = configparser.ConfigParser()
	config['DEFAULT']['RSS_URL'] = 'citr.ca/radio/democracy-watch/'
	config['DEFAULT']['BASE_DIR'] = '/media/arman/Data1/CITR/DemocracyWatch/'
	config['DEFAULT']['EXT_INPUT_AUDIO'] = '.mp3'
	config['DEFAULT']['EXT_OUTPUT_VIDEO'] = '.mkv'
	config['DEFAULT']['IMAGE'] = 'democracy_watch.jpg'
	config['DEFAULT']['START_DATE'] = date_str
	config['DEFAULT']['CHUNK_SIZE'] = '1024'

	with open('/home/arman/projects/rss_to_youtube/config.ini', 'w') as configfile:
		config.write(configfile)


def get_config():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config


def update_date(date):
	config = configparser.ConfigParser()
	config.read('config.ini')
	date = max(parser.parse(config['DEFAULT']['START_DATE']), date)
	config['DEFAULT']['START_DATE'] = str(date)
	with open('/home/arman/projects/rss_to_youtube/config.ini', 'w+') as configfile:
		config.write(configfile)

