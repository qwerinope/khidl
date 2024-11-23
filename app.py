EXAMPLEID="katamari-damacy-reroll-ps4-switch-windows-xbox-one-gamerip-2018"

from lib.args import *
from lib.soundtrack import *
from lib.downloader import *

if __name__ == "__main__": # Start: only executes when running script directly
    soundtrack, outputdir, requestedformat = getArguments()
    ost = Soundtrack(soundtrack)

    if requestedformat and requestedformat in ost.formats:
        format = requestedformat
    else:
        format = 'mp3'

    if not outputdir:
        outputdir = ost.name

    filelist = preDownloadMusic(ost, format)
    filelist = filelist + ost.images
    download(filelist, outputdir)
    print(f"Downloaded '{ost.name}' to '{outputdir}'")
