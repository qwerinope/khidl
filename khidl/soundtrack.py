BASEURL="https://downloads.khinsider.com"
import requests, bs4, sys

class Soundtrack:
    """ Representative of a soundtrack on KHinsider

    Attributes:
    id: id of the soundtrack
    url: the url of the soundtrack
    pageinstance: an instance of beautifulsoup with the soundtrack page loaded
    name: soundtrack name
    images: array of images
    formats: containers/codecs the album is available in (mp3 + flac or m4a)
    tracks: array of tracknames
    """

    def __init__(self, id:str):
        try:
            self.id = id
            self.url = self._getURL()
            self.pageinstance = self._getPage()
            self.name = self._getName()
            self.images = self._getImages()
            self.formats = self._getFormats()
            self.tracks = self._getTracks()
        except OSTParsingError:
            print("An error occured!\nPlease leave an issue at https://github.com/qweri0p/khidl/issues", file=sys.stderr)
            exit(1)
        except OSTNotFound as e:
            print(e, file=sys.stderr)
            self.id = None
            return

    def _getURL(self):
        return f'{BASEURL}/game-soundtracks/album/{self.id}'

    def _getPage(self):
        raw = requests.get(self.url)
        firstparser = bs4.BeautifulSoup(raw.text, 'html.parser')
        
        if firstparser:
            parser = firstparser
        else:
            raise OSTParsingError

        return parser

    def _getName(self):
        # NOTE: This could also be done by using the information txt file. However, i don't give a shit. Maybe later I will.
        parser = self.pageinstance

        if parser.h2 and parser.h2.string:
            ostname = parser.h2.string
        else:
            raise OSTParsingError

        if ostname == "Ooops!":
            raise OSTNotFound(self)

        return ostname

    def _getImages(self):
        parser = self.pageinstance
        images = []
        imagecontainers = parser.find_all("div", "albumImage") or []

        for image in imagecontainers:
            images.append(image.find('a').get('href'))

        return images

    def _getFormats(self):
        parser = self.pageinstance
        header = parser.select_one('#songlist_header')
        columns = header.find_all('b') if header else []
        formats = [
            col.string.lower()
            for col in columns
            if col.string and col.string.lower() in {'mp3', 'm4a', 'flac'}
        ]
        return formats

    def _getTracks(self):
        parser = self.pageinstance
        songlist = parser.select_one('#songlist')

        if not songlist:
            raise OSTParsingError

        anchors = [
            trackEntry.find('a').get('href')   # find one anchor tag
            for trackEntry in songlist.find_all('tr')   # for every single table row
            if trackEntry.find('a')                     # skip the header and footer
        ]
        trackURLs = [f'{BASEURL}{tracklink}' for tracklink in anchors]
        return trackURLs

class OSTParsingError(Exception):
    """This should NEVER EVER be triggered. If khinsider's website changes this might get set off but that's very unlikely"""

class OSTNotFound(Exception):
    def __init__(self, soundtrack, *args):
        super().__init__(*args)
        self.message = f"{soundtrack.id} Not found. Please make sure you correctly set the ID"

    def __str__(self):
        return self.message
