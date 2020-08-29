from src.model.request import Request
from src.model import converter
from src.model import downloader
from src.util import create_filename, create_path
from src.constants import SUMMARY_TEXT, DATE_TEXT


def process(episode, request: Request):
    filename = create_filename(episode.title)

    image_path = request.image
    audio_path = create_path(request.base_dir, filename, request.input_audio_ext)
    video_path = create_path(request.base_dir,  filename, request.output_video_ext)
    description = f'{SUMMARY_TEXT}: {episode.summary}, {DATE_TEXT}:  {episode.published}'

    downloader.download(episode, audio_path, request.chunk_size)
    converter.to_video(image_path, audio_path, video_path, description)


