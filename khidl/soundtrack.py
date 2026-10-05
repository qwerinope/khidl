BASEURL = "https://downloads.khinsider.com"
import requests, bs4, sys


class Soundtrack:
    """Representative of a soundtrack on KHinsider

    Attributes:
    id: id of the soundtrack
    url: the url of the soundtrack
    pageinstance: an instance of beautifulsoup with the soundtrack page loaded
    name: soundtrack name
    images: array of images
    formats: containers/codecs the album is available in (mp3 + flac or m4a)
    tracks: array of tracknames
    """

    def __init__(self, id: str):
        try:
            self.id = id
            self.url = self._getURL()
            self.pageinstance = self._getPage()
            self.name = self._getName()
            self.images = self._getImages()
            self.formats = self._getFormats()
            self.tracks = self._getTracks()
        except OSTWebsiteUnavailable as e:
            print(
                f"Could not reach KHInsider while loading soundtrack '{id}'. "
                "Check your internet connection, DNS, proxy, and firewall settings. "
                f"Request details: {e}",
                file=sys.stderr,
            )
            sys.exit(1)
        except OSTParsingError as e:
            print(
                f"Could not load soundtrack '{id}'. "
                "KHInsider responded, but its page did not have the expected format. "
                f"The website may have changed: {e}",
                file=sys.stderr,
            )
            sys.exit(1)
        except OSTNotFound as e:
            print(e, file=sys.stderr)
            self.id = None
            return

    def _getURL(self):
        return f"{BASEURL}/game-soundtracks/album/{self.id}"

    def _getPage(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Encoding": "identity",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Site": "same-site",
        }

        try:
            raw = requests.get(self.url, headers=headers, timeout=10)
            raw.raise_for_status()
        except (requests.ConnectionError, requests.Timeout) as e:
            raise OSTWebsiteUnavailable(str(e)) from e
        except requests.RequestException as e:
            raise OSTParsingError(f"Request failed: {e}") from e
        firstparser = bs4.BeautifulSoup(raw.text, "html.parser")

        if firstparser:
            parser = firstparser
        else:
            raise OSTParsingError("The response body was empty.")

        return parser

    def _getName(self):
        # NOTE: This could also be done by using the information txt file. However, i don't give a shit. Maybe later I will.
        parser = self.pageinstance
        if parser.h2 and parser.h2.string:
            ostname = parser.h2.string
        else:
            raise OSTParsingError("The page did not contain a soundtrack title.")

        if ostname == "Ooops!":
            raise OSTNotFound(self)

        return ostname

    def _getImages(self):
        parser = self.pageinstance
        images = []
        imagecontainers = parser.find_all("div", "albumImage") or []

        for image in imagecontainers:
            images.append(image.find("a").get("href"))

        return images

    def _getFormats(self):
        parser = self.pageinstance
        header = parser.select_one("#songlist_header")
        columns = header.find_all("b") if header else []
        formats = [
            col.string.lower()
            for col in columns
            if col.string and col.string.lower() not in {"#", "song name"}
        ]
        return formats

    def _getTracks(self):
        parser = self.pageinstance
        songlist = parser.select_one("#songlist")

        if not songlist:
            raise OSTParsingError("The page did not contain a track list.")

        anchors = [
            trackEntry.find("a").get("href")  # find one anchor tag
            for trackEntry in songlist.find_all("tr")  # for every single table row
            if trackEntry.find("a")  # skip the header and footer
        ]
        trackURLs = [f"{BASEURL}{tracklink}" for tracklink in anchors]
        return trackURLs


class OSTParsingError(Exception):
    """The soundtrack page could not be loaded or parsed."""


class OSTWebsiteUnavailable(Exception):
    """KHInsider could not be reached from the user's environment."""


class OSTNotFound(Exception):
    def __init__(self, soundtrack, *args):
        super().__init__(*args)
        self.message = (
            f"{soundtrack.id} Not found. Please make sure you correctly set the ID"
        )

    def __str__(self):
        return self.message
