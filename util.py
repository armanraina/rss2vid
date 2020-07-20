import ffmpeg
from pathvalidate import sanitize_filename
import os.path
import validators
from dateutil import parser
from tzlocal import get_localzone
import sys


def create_filename(title):
    return sanitize_filename(title)


def create_path(directory, filename, extension):
    return os.path.join(directory, filename + extension)


def create_video_stream(image_stream, audio_stream, out_stream):
    audio = ffmpeg.input(audio_stream)
    image = ffmpeg.input(image_stream, loop=1, framerate=1)
    out = ffmpeg.output(
        audio, image, out_stream,
        shortest=None, preset='veryslow', crf=0,
        **{'c:a': 'copy', 'c:v': 'libx264'})
    out.run()


def validate_url(url: str):
    return validators.url(url) or validators.url(f'https://{url}')


def validate_image(image: str):
    return os.path.isfile(image) and os.path.splitext(image)[-1].lower() in ['.png', '.jpg', '.jpeg']


def validate_directory(directory: str):
    return os.path.isdir(directory)


def validate_date(date: str):
    try:
        parser.parse(date)
    except (ValueError, OverflowError):
        return False
    return True


def create_local_datetime(string: str):
    if validate_date(string):
        parsed_start_date = parser.parse(string)
        if not parsed_start_date.tzinfo:
            local_tz = get_localzone()
            parsed_start_date = local_tz.localize(parsed_start_date)
        return parsed_start_date
    else:
        return None


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def data_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
