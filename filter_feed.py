from util import getFeed, createVideo
from datetime import timedelta, timezone, datetime
from dateutil import parser
import pprint
from config_manager import initializeConfig, updateDate
CITR_URL = 'citr.ca/radio/democracy-watch/'

pp = pprint.PrettyPrinter(indent=4)


def get_filtered_feed(feed, start_date=None):
	if start_date == None:
	 start_date =  datetime.min.replace(tzinfo=timezone.utc)
	for episode in feed.entries:
		published = parser.parse(episode.published)
		if published > start_date:
			yield episode 
			
feed = getFeed(CITR_URL)
#get_filtered_feed(feed)
#pp.pprint(feed.entries[1])

updateDate(parser.parse(feed.entries[0].published))
