import requests
from tqdm import tqdm


def download(url, output_path, chunk_size: int, stream: bool = True):
    response = requests.get(url, stream=stream)
    chunk_size = chunk_size ** 2
    progress_bar = tqdm(unit="B", total=int(response.headers['Content-Length']))
    with open(output_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
            progress_bar.update(chunk_size)



