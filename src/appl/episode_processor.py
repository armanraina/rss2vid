from src.appl.request import Request
from src.infr import downloader, converter
from src.util import create_filename, create_path
from src.constants import SUMMARY_TEXT, DATE_TEXT
from src.model.episode import Episode


def process(episode: Episode, request: Request):
    filename = create_filename(episode.get_title())

    image_path = request.image
    audio_path = create_path(request.base_dir, filename, request.input_audio_ext)
    video_path = create_path(request.base_dir,  filename, request.output_video_ext)
    description = f'{SUMMARY_TEXT}: {episode.get_summary()}, {DATE_TEXT}:  {episode.get_published()}'

    downloader.download(episode.get_url(), audio_path, request.chunk_size)
    converter.to_video(image_path, audio_path, video_path, description)


