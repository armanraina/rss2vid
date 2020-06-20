import PySimpleGUI as sg
from config_manager import get_config
from Request import Request
from Downloader import Downloader
from Converter import Converter
from RequestProcessor import RequestProcessor
from FeedProvider import FeedProvider
from EpisodeProcessor import EpisodeProcessor
from dateutil import parser
from tzlocal import get_localzone
from FeedSearcher import FeedSearcher

config = get_config()
rss_url = config['DEFAULT']['RSS_URL']
start_date = parser.parse(config['DEFAULT']['START_DATE'])
base_dir = config['DEFAULT']['BASE_DIR']
input_audio_ext = config['DEFAULT']['EXT_INPUT_AUDIO']
output_video_ext = config['DEFAULT']['EXT_OUTPUT_VIDEO']
image = config['DEFAULT']['IMAGE']
chunk_size = int(config['DEFAULT']['CHUNK_SIZE'])

default_date_m_d_y = (start_date.month, start_date.day, start_date.year)

# All the stuff inside your window.
AUDIO_RADIO_GROUP = 'AUDIO_RADIO_GROUP'
VIDEO_RADIO_GROUP = 'VIDEO_RADIO_GROUP'

layout = [
    [sg.T('RSS URL'), sg.I(default_text=rss_url, key='rss_url')],
    [sg.T('Output Directory'), sg.I(key='base_dir', default_text=base_dir), sg.FolderBrowse(initial_folder=base_dir)],
    [sg.T('Image'), sg.Input(key='image', default_text=image), sg.FileBrowse(initial_folder=base_dir)],
    [sg.T('Audio Format'), sg.Radio(input_audio_ext, default=True, key='input_audio_ext', group_id=AUDIO_RADIO_GROUP)],
    [sg.T('Video Format'), sg.Radio(output_video_ext, default=True, key='output_video_ext', group_id=VIDEO_RADIO_GROUP)],
    [sg.T('Start Date'), sg.I(key='start_date', default_text=str(start_date)),
     sg.CalendarButton(default_date_m_d_y=default_date_m_d_y, button_text='Pick Date')],
    [sg.T('Chunk Size'), sg.Slider(range=(1024, 2048), default_value=chunk_size, key='chunk_size')],
    [sg.Button('Ok'), sg.Button('Cancel')]
    ]

# Create the Window
window = sg.Window('RSS2Vid', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    print(values)
    rss_url = values['rss_url']
    start_date = values['start_date']
    base_dir = values['base_dir']
    input_audio_ext = values['input_audio_ext'] and input_audio_ext
    output_video_ext = values['output_video_ext'] and output_video_ext
    image = values['image']
    chunk_size = values['chunk_size']

    parsed_start_date = parser.parse(start_date)
    if not parsed_start_date.tzinfo:
        local_tz = get_localzone()
        parsed_start_date = local_tz.localize(parsed_start_date)

    request = Request(rss_url,
                      parsed_start_date,
                      base_dir,
                      input_audio_ext,
                      output_video_ext,
                      image,
                      int(chunk_size))

    downloader = Downloader(request.chunk_size)
    converter = Converter()
    feed_searcher = FeedSearcher()
    feed_provider = FeedProvider(feed_searcher,request.rss_url)
    episode_processor = EpisodeProcessor(converter, downloader)
    request_processor = RequestProcessor(feed_provider, episode_processor)
    request_processor.process(request)

    window.close()

