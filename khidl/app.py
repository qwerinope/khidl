import sys
from .args import getArguments
from .soundtrack import Soundtrack
from .downloader import preDownloadMusic, download, DLParseException
from .search import search, SearchParsingError, SearchNoResults

class FormatNotAvailable(Exception):
    """The format the user wanted is not provided by KHInsider"""
    def __init__(self, soundtrack, wantedFormat, *args):
        super().__init__(*args)
        self.message = f"{wantedFormat} isn't available on {soundtrack.name}. Please try a different format"
    def __str__(self):
        return self.message

def downloadManager(soundtrackId, wantedFormat, outDir, getImages):
    ost = Soundtrack(soundtrackId)

    if ost.id == None:
        return 'err'

    if wantedFormat not in ost.formats:
        raise FormatNotAvailable(ost, wantedFormat)

    filelist = preDownloadMusic(ost, wantedFormat)
    outputDir = outDir if outDir else ost.name
    if getImages:
        filelist += ost.images
    download(filelist, outputDir)
    print(f"Downloaded '{ost.name}' to '{outputDir}'")
    return 'ok'

def CLI():
    command, data = getArguments()
    match command:
        case "download":
            # The data tuple consists of: (soundtrackId, wantedFormat, outDir, getImages)
            try:
                status = downloadManager(*data)
                if status == "err":
                    exit(1)
            except FormatNotAvailable as e:
                print(e, file=sys.stderr)
                exit(1)
            except DLParseException:
                print("An error occured!\nPlease leave an issue at https://github.com/qweri0p/khidl/issues", file=sys.stderr)
                exit(1)

        case "batch":
            # The data array contains tuples that consist of: (soundtrackId, wantedFormat, outDir, getImages)
            print(f"Succesfully parsed configuration.\nDownloading {len(data)} soundtracks.")

            for ost in data:
                try:
                    status = downloadManager(*ost)
                    if status == "err":
                        continue
                except FormatNotAvailable as e:
                    print(e)
                    continue
                except DLParseException:
                    print("An error occured!\nPlease leave an issue at https://github.com/qweri0p/khidl/issues", file=sys.stderr)
                    continue

        case "search":
            # Data is a URL to the search page on KHInsider
            try:
                search(data)
            except SearchParsingError:
                print("An error occured!\nPlease leave an issue at https://github.com/qweri0p/khidl/issues", file=sys.stderr)
                exit(1)
            except SearchNoResults:
                print("No soundtracks matched the requests.", file=sys.stderr)
                exit(1)
