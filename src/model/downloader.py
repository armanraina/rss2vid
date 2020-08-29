import requests
from tqdm import tqdm
from src.model.download_exception import DownloadException


def download(episode, audio_path, chunk_size: int, stream: bool = True):
    if __validate_episode(episode) and __get_mp3_link(episode):
        response = requests.get(__get_mp3_link(episode), stream=stream)
        chunk_size = chunk_size ** 2
        progress_bar = tqdm(unit="B", total=int(response.headers['Content-Length']))
        with open(audio_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
                progress_bar.update(chunk_size)
    else:
        raise DownloadException(f'{__name__} : Format not supported: {episode}')


def __get_mp3_link(episode):
    links = [enclosure.href for enclosure in episode.enclosures if enclosure.type == u'audio/mpeg']
    if not links:
        return None
    else:
        return links[0]


def __validate_episode(episode):
    return bool(episode.enclosures)
