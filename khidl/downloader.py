from urllib.parse import unquote
import re
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm
from .soundtrack import Soundtrack


def preDownloadMusic(soundtrack: Soundtrack, format: str):
    urls = []

    for index, track in enumerate(soundtrack.tracks):
        print(f"\rPreparing download: {index + 1}/{len(soundtrack.tracks)}", end="")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Encoding": "identity",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Site": "same-site",
        }
        try:
            r = requests.get(track, headers=headers)
            r.raise_for_status()
        except requests.RequestException as e:
            raise DLParseException(
                f"Could not load track {index + 1} from {track}: {e}"
            ) from e
        parser = BeautifulSoup(r.text, "html.parser")
        dllink = parser.select_one(".songDownloadLink")

        if not dllink:
            raise DLParseException(
                f"Could not find a download link for track {index + 1} ({track})."
            )

        dlanchor = dllink.parent

        if not dlanchor:
            raise DLParseException(
                f"Could not find the download URL for track {index + 1} ({track})."
            )

        originURL = dlanchor.get("href")

        if not originURL:
            raise DLParseException(
                f"The download URL for track {index + 1} was empty ({track})."
            )

        base = str(originURL).rsplit("/", 1)[0]
        trackname = originURL.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        url = f"{base}/{trackname}.{format}"
        try:
            exists = requests.head(url)
        except requests.RequestException as e:
            raise DLParseException(
                f"Could not check whether track {index + 1} is available as "
                f"'{format}': {e}"
            ) from e
        if exists.status_code != 200:
            urls.append(f"{base}/{trackname}.mp3")
            print(
                f"\rCannot find track {index + 1} '{unquote(trackname)}' in {format} format. Downloading the mp3 version instead."
            )
        else:
            urls.append(url)

    return urls


def download(dlurls: list[str], rawOutDir: str):
    outDir = cleanPath(rawOutDir)
    output = Path(outDir)
    output.mkdir(exist_ok=True)
    for url in dlurls:
        fname = cleanPath(unquote(url.rsplit("/", 1)[-1]))

        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise DLParseException(f"Could not download '{fname}': {e}") from e
        total = int(resp.headers.get("content-length", 0))
        with (
            open(f"{output}/{fname}", "wb") as file,
            tqdm(
                desc=fname,
                total=total,
                unit="iB",
                bar_format="{desc}: {percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} [{rate_fmt}]",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar,
        ):
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)


class DLParseException(Exception):
    """A soundtrack page or track download could not be processed."""


"""removes illegal characters from path and filenames"""


def cleanPath(path: str) -> str:
    if os.environ.get("TERMUX_VERSION") is not None:
        return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", path)
    match os.name:
        case "nt":
            # eww 🤮🤮🤮🤮
            return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", path)
        case _:
            return re.sub(r"[/]", "_", path)
