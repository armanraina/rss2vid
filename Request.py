from dateutil import parser


class Request:
    def __init__(self, rss_url, start_date, base_dir, input_audio_ext, output_video_ext, image, chunk_size):
        self.rss_url = rss_url
        self.start_date = start_date
        self.base_dir = base_dir
        self.input_audio_ext = input_audio_ext
        self.output_video_ext = output_video_ext
        self.image = image
        self.chunk_size = chunk_size

    def __init__(self, config):
        self.rss_url = config['DEFAULT']['RSS_URL']
        self.start_date = parser.parse(config['DEFAULT']['START_DATE'])
        self.base_dir = config['DEFAULT']['BASE_DIR']
        self.input_audio_ext = config['DEFAULT']['EXT_INPUT_AUDIO']
        self.output_video_ext = config['DEFAULT']['EXT_OUTPUT_VIDEO']
        self.image = config['DEFAULT']['IMAGE']
        self.chunk_size = int(config['DEFAULT']['CHUNK_SIZE'])

