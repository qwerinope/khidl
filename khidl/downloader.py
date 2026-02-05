from urllib.parse import unquote
import re
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List
from tqdm import tqdm
from .soundtrack import Soundtrack

def preDownloadMusic(soundtrack:Soundtrack, format:str):
    urls = []

    for index, track in enumerate(soundtrack.tracks):
        print("\rPreparing download: {}/{}".format(index+1, len(soundtrack.tracks)), end="")
        headers = {"User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Encoding": "identity",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Site":"same-site"}
        r = requests.get(track, headers=headers)
        parser = BeautifulSoup(r.text, 'html.parser')
        dllink = parser.select_one('.songDownloadLink')

        if not dllink:
            raise DLParseException

        dlanchor = dllink.parent

        if not dlanchor:
            raise DLParseException

        originURL = dlanchor.get('href').__str__()

        if not originURL:
            raise DLParseException

        base = str(originURL).rsplit(str('/'), 1)[0]
        trackname = originURL.rsplit(str('/'), 1)[-1].rsplit(str('.'), 1)[0]
        url = f'{base}/{trackname}.{format}'
        exists = requests.head(url)
        if (exists.status_code != 200):
            urls.append(f'{base}/{trackname}.mp3')
            print(f"\rCannot find track {index+1} '{unquote(trackname)}' in {format} format. Downloading the mp3 version instead.")
        else:
            urls.append(url)


    return urls

def download(dlurls:List[str], outDir:str):
    output = Path(outDir)
    output.mkdir(exist_ok=True)
    for url in dlurls:
        fname = unquote(url.rsplit(str('/'), 1)[-1])
        
        if os.name == "nt":
            fname = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", fname)

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
