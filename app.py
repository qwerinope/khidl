EXAMPLEID="katamari-damacy-reroll-ps4-switch-windows-xbox-one-gamerip-2018"

from lib.args import getArguments
from lib.soundtrack import Soundtrack
from lib.downloader import preDownloadMusic, download
from lib.search import search

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

if __name__ == "__main__": # Start: only executes when running script directly
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

