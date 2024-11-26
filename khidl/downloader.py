from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Literal
from tqdm import tqdm
from .soundtrack import Soundtrack

def preDownloadMusic(soundtrack:Soundtrack, format:Literal['mp3', 'flac', 'm4a']):
    print(f"Downloading '{soundtrack.name}'...")
    urls = []

    for index, track in enumerate(soundtrack.tracks):
        print("\rPreparing download: {}/{}".format(index+1, len(soundtrack.tracks)), end="")
        r = requests.get(track)
        parser = BeautifulSoup(r.text, 'html.parser')
        dllink = parser.select_one('.songDownloadLink')

        if not dllink:
            raise DLParseException

        dlanchor = dllink.parent

        if not dlanchor:
            raise DLParseException

        originURL = dlanchor.get('href')

        if not originURL:
            raise DLParseException

        base = str(originURL).rsplit(str('/'), 1)[0]
        urls.append(f'{base}/{unquote(track.rsplit(str('/'), 1)[-1].rsplit(str('.'), 1)[0])}.{format}')

    return urls

def download(dlurls:List[str], outDir:str):
    output = Path(outDir)
    output.mkdir(exist_ok=True)
    for url in dlurls:
        fname = unquote(url.rsplit(str('/'), 1)[-1])
        resp = requests.get(url, stream=True)
        total = int(resp.headers.get('content-length', 0))
        with open(f'{output}/{fname}', 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            bar_format="{desc}: {percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} [{rate_fmt}]",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

class DLParseException(Exception):
    """This should NEVER EVER be triggered. If khinsider's website changes this might get set off but that's very unlikely"""
