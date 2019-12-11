import requests
from tqdm import tqdm


class Downloader:
    def __init__(self, chunk_size: int, stream: bool = True):
        self.chunk_size = chunk_size
        self.stream = stream

    def download(self, episode, audio_path):
        if self.__validate_episode(episode) and self.__get_mp3_link(episode):
            response = requests.get(self.__get_mp3_link(episode), stream=self.stream)
            chunk_size = self.chunk_size ** 2
            progress_bar = tqdm(unit="B", total=int(response.headers['Content-Length']))
            with open(audio_path, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
                    progress_bar.update(chunk_size)
        else:
            print('Downloader: Episode Not Supported')

    @staticmethod
    def __get_mp3_link(episode):
        links = [enclosure.href for enclosure in episode.enclosures if enclosure.type == u'audio/mpeg']
        if not links:
            return None
        else:
            return links[0]

    @staticmethod
    def __validate_episode(episode):
        return bool(episode.enclosures)
