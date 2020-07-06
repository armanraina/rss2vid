import datetime
import validators


class Request:
    def __init__(self, rss_url: str,
                 start_date: datetime,
                 base_dir: str,
                 input_audio_ext: str,
                 output_video_ext: str,
                 image,
                 chunk_size: int = 1024):
        self.rss_url = rss_url
        self.start_date = start_date
        self.base_dir = base_dir
        self.input_audio_ext = input_audio_ext
        self.output_video_ext = output_video_ext
        self.image = image
        self.chunk_size = chunk_size