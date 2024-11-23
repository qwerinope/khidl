def getArguments():
    import argparse
    parser = argparse.ArgumentParser(description="Download videogame soundtracks from downloads.khinsider.com")
    parser.add_argument("request", help="the soundtrack name or url the user wishes to download", nargs=1)
    parser.add_argument("output", help="store the resulting music in a specified directory", default=None, nargs='?')
    parser.add_argument("-f", "--format", help="the requested audio format, can be 'mp3', 'flac' or 'm4a'", type=str, choices=['mp3', 'flac', 'm4a'])
    # TODO: options for different audio formats, to just search, and maybe even do the json parsing

    args = parser.parse_args()
    ostid = args.request[0].rsplit(str('/'),1)[0]
    return ostid, args.output, args.format
