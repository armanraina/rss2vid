from src.model.response import Response
from src.model.request import Request
from src.constants import MKV_EXT, MIN_DATE_STR, LOADING_STRING, COUNTING_STRING, MP3_EXT, DEFAULT_DATE_STR
from src.util import localize_datetime
from src.model.progress_updater import ProgressUpdater
from src.model.request_processor import RequestProcessor
import click


@click.command()
@click.option('--image',
              prompt='Image file',
              help='Image file for video.')
@click.option('--url',
              prompt='Podcast URL',
              help='The URL of the RSS feed of the podcast.')
@click.option('--output_dir',
              prompt='Output location',
              help='Output location for video.')
@click.option('--start_date',
              default=MIN_DATE_STR,
              prompt='Start date',
              help='Filter out episodes prior to this date.',
              type=click.DateTime())
@click.option('--video_format',
              default=MKV_EXT,
              help='Output format for video.')
def hello(image, url, output_dir, video_format, start_date):
    request = Request(url,
                      localize_datetime(start_date),
                      output_dir,
                      MP3_EXT,
                      video_format,
                      image)

    progress_updater = ProgressUpdater(update_progress)
    request_processor = RequestProcessor(progress_updater)
    response = request_processor.process(request)
    print(response)


def update_progress(progress: int, total: int):
    if progress > 0:
        print(LOADING_STRING.format(str(progress), str(total)))
    else:
        print(COUNTING_STRING)


if __name__ == '__main__':
    hello()
