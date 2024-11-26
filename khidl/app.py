from .args import getArguments
from .soundtrack import Soundtrack
from .downloader import preDownloadMusic, download
from .search import search

class FormatNotAvailable(Exception):
    pass

def downloadManager(soundtrackId, wantedFormat, outDir, getImages):
    ost = Soundtrack(soundtrackId)

    if wantedFormat not in ost.formats:
        raise FormatNotAvailable

    filelist = preDownloadMusic(ost, wantedFormat)
    outputDir = outDir if outDir else ost.name
    if getImages:
        filelist += ost.images
    download(filelist, outputDir)
    print(f"Downloaded '{ost.name}' to '{outputDir}'")

def CLI():
    command, data = getArguments()
    match command:
        case "download":
            # The data tuple consists of: (soundtrackId, wantedFormat, outDir, getImages)
            downloadManager(*data)

        case "batch":
            # The data array contains tuples that consist of: (soundtrackId, wantedFormat, outDir, getImages)
            print(f"Succesfully parsed configuration.\nDownloading {len(data)} soundtracks.")
            for ost in data:
                downloadManager(*ost)
        case "search":
            # Data is a URL to the search page on KHInsider
            search(data)

if __name__ == "__main__": # Start: only executes when running script directly
    CLI()
