from src.model import Request
from src.model import Converter
from src.model import Downloader
from src.util import create_filename, create_path


class EpisodeProcessor:
    SUMMARY_TEXT = 'SUMMARY'
    DATE_TEXT = 'DATE'

    def __init__(self, converter: Converter, downloader: Downloader, request: Request = None):
        self.request = request
        self.converter = converter
        self.downloader = downloader

    def process(self, episode):
        if self.request:
            filename = create_filename(episode.title)

            image_path = self.request.image
            audio_path = create_path(self.request.base_dir, filename, self.request.input_audio_ext)
            video_path = create_path(self.request.base_dir,  filename, self.request.output_video_ext)
            description = f'{self.SUMMARY_TEXT}: {episode.summary}, {self.DATE_TEXT}:  {episode.published}'

            self.downloader.download(episode, audio_path)
            self.converter.to_video(image_path, audio_path, video_path, description)

    def set_request(self, request: Request):
        self.request = request

