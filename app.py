EXAMPLEID="katamari-damacy-reroll-ps4-switch-windows-xbox-one-gamerip-2018"

from lib.args import *
from lib.soundtrack import *
from lib.downloader import *

def downloadManager(soundtrackId, wantedFormat, outDir, getImages):
    ost = Soundtrack(soundtrackId)
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
            # The data object consists of: (soundtrackId, wantedFormat, outDir, getImages)
            downloadManager(data[0], data[1], data[2], data[3])

        case "batch":
            # The data object consists of: [{soundtrack: id, format: wantedFormat, output: outDir, images: getImages}]
            print(f"Succesfully parsed configuration.\nDownloading {len(data)} soundtracks.")
            for ost in data:
                downloadManager(ost['soundtrack'], ost['format'], ost['output'], ost['images'])
