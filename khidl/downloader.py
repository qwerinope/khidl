from urllib.parse import unquote
import re
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm
from .soundtrack import Soundtrack

def preDownloadMusic(soundtrack:Soundtrack, format:str):
    urls = []

    for index, track in enumerate(soundtrack.tracks):
        print(f"\rPreparing download: {index+1}/{len(soundtrack.tracks)}", end="")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
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

        base = str(originURL).rsplit('/', 1)[0]
        trackname = originURL.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        url = f'{base}/{trackname}.{format}'
        exists = requests.head(url)
        if (exists.status_code != 200):
            urls.append(f'{base}/{trackname}.mp3')
            print(f"\rCannot find track {index+1} '{unquote(trackname)}' in {format} format. Downloading the mp3 version instead.")
        else:
            urls.append(url)


    return urls

def download(dlurls:list[str], rawOutDir:str):
    outDir = cleanPath(rawOutDir)
    output = Path(outDir)
    output.mkdir(exist_ok=True)
    for url in dlurls:
        fname = cleanPath(unquote(url.rsplit('/', 1)[-1]))

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


"""removes illegal characters from path and filenames"""
def cleanPath(path:str) -> str:
    if os.environ.get("TERMUX_VERSION") is not None:
        return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", path)
    match os.name:
        case 'nt':
            # eww 🤮🤮🤮🤮
            return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", path)
        case _:
            return re.sub(r'[/]', "_", path)
