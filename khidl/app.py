import sys
from .args import getArguments
from .soundtrack import Soundtrack
from .downloader import preDownloadMusic, download, DLParseException
from .search import search, SearchParsingError, SearchNoResults


class FormatNotAvailable(Exception):
    """The format the user wanted is not provided by KHInsider"""

    def __init__(self, soundtrack, wantedFormat, *args):
        super().__init__(*args)
        self.message = (
            f"Format '{wantedFormat}' is not available for '{soundtrack.name}'. "
            f"Available formats: {', '.join(soundtrack.formats)}."
        )

    def __str__(self):
        return self.message


def downloadManager(soundtrackId, wantedFormat, outDir, getImages):
    if not getImages and wantedFormat == "nomusic":
        print(
            "Nothing to download: music is disabled and --no-images was specified.",
            file=sys.stderr,
        )
        return "err"

    ost = Soundtrack(soundtrackId)

    if ost.id == None:
        return "err"

    filelist = []

    print(f"Downloading '{ost.name}'...")

    if wantedFormat != "nomusic":
        if wantedFormat not in ost.formats:
            raise FormatNotAvailable(ost, wantedFormat)

        filelist = preDownloadMusic(ost, wantedFormat)

    outputDir = outDir if outDir else ost.name
    if getImages:
        filelist += ost.images

    download(filelist, outputDir)
    print(f"Downloaded '{ost.name}' to '{outputDir}'")
    return "ok"


def CLI():
    command, data = getArguments()
    match command:
        case "download":
            # The data tuple consists of: (soundtrackId, wantedFormat, outDir, getImages)
            try:
                status = downloadManager(*data)
                if status == "err":
                    sys.exit(1)
            except FormatNotAvailable as e:
                print(e, file=sys.stderr)
                sys.exit(1)
            except DLParseException as e:
                print(f"Could not download the soundtrack: {e}", file=sys.stderr)
                sys.exit(1)

        case "batch":
            # The data array contains tuples that consist of: (soundtrackId, wantedFormat, outDir, getImages)
            print(
                f"Successfully parsed configuration.\nDownloading {len(data)} soundtracks."
            )

            for ost in data:
                try:
                    status = downloadManager(*ost)
                    if status == "err":
                        continue
                except FormatNotAvailable as e:
                    print(e, file=sys.stderr)
                    continue
                except DLParseException as e:
                    print(
                        f"Could not download this soundtrack: {e}",
                        file=sys.stderr,
                    )
                    continue

        case "search":
            # Data is a tuple with (query, jsonfilename(optional))
            try:
                search(*data)
            except SearchParsingError as e:
                print(f"Could not parse the search results: {e}", file=sys.stderr)
                sys.exit(1)
            except SearchNoResults:
                print("No soundtracks matched your search.", file=sys.stderr)
                sys.exit(1)
