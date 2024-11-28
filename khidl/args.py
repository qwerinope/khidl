import argparse, json, sys, requests
from pathlib import Path
from jsonschema import validate, ValidationError

EXAMPLECONFIG = {
    "$schema": "https://raw.githubusercontent.com/qweri0p/khdl/refs/heads/main/schema.json",
    "defaultFormat": "mp3",
    "soundtracks": [
        {
            "soundtrack": "katamari-damacy-reroll-ps4-switch-windows-xbox-one-gamerip-2018",
            "format": "mp3",
            "output": "Katamari Damacy",
        },
        {
            "soundtrack": "https://downloads.khinsider.com/game-soundtracks/album/plants-vs.-zombies",
            "format": "flac",
            "images": False
        },
        "super-mario-64-soundtrack"
    ]
}

def getArguments():
    # This function passes execution over to a helper function that parses all arguments.
    # It always responds with 2 variables: a Literate of type "search", "batch" or "download" and something else.
    parser = argparse.ArgumentParser(description="Download videogame soundtracks from downloads.khinsider.com")
    subparser = parser.add_subparsers(dest="command", required=True)

    downloadcmd = subparser.add_parser('download', help="download a specific soundtrack")
    downloadcmd.set_defaults(func=downloadParser)
    downloadcmd.add_argument("request", help="the soundtrack name or url the user wishes to download", nargs=1, type=str)
    downloadcmd.add_argument("output", help="store the resulting music in a specified directory", default=None, nargs='?', type=str)
    downloadcmd.add_argument("-f", "--format", help="the requested audio format, can be 'mp3', 'flac' or 'm4a'", type=str, choices=['mp3', 'flac', 'm4a'], default='mp3', nargs='?')
    downloadcmd.add_argument("--no-images", help="don't download the images on the specific soundtrack", action='store_true', default=False)

    jsoncmd = subparser.add_parser('batch', help="download multiple pre-defined soundtracks", description="download multiple soundtracks specified in a configuration file")
    jsoncmd.set_defaults(func=batchParser)
    jsoncmd.add_argument('-i', '--init', help="create a default configuration for batch downloading", action='store_true', default=False)

    searchcmd = subparser.add_parser('search', help="search KHInsider for soundtracks", description="use the search function on KHInsider and list all found soundtracks")
    searchcmd.set_defaults(func=searchParser)
    searchcmd.add_argument('query', help="search query", nargs='+', type=str)
    searchcmd.add_argument('--song', help="search for soundtracks containing a specific song", action='store_true', default=False)

    args = parser.parse_args()
    return args.func(args)

def downloadParser(args):
    if 'downloads.khinsider.com' in  args.request[0]:
        ostid = args.request[0].rsplit(str('/'), 1)[-1]
    else:
        ostid = args.request[0]

    return "download" , (ostid, args.format, args.output, args.no_images)

def batchParser(args):
    cfgfile = Path('soundtracks.json')
    if args.init:
        cfgfile.write_text(json.dumps(EXAMPLECONFIG, indent=4))
        print(f"Written default config to '{cfgfile}'")
        exit(0)

    if not cfgfile.exists():
        print(f"There is no configuration at '{cfgfile}'.\nPlease create a config using the '--init' argument, then modify it.", file=sys.stderr)
        exit(1)
    try:
        cfg = json.loads(cfgfile.read_text())
    except json.JSONDecodeError:
        print(f"The '{cfgfile}' file has a JSON syntax error.", file=sys.stderr)
        exit(1)

    r = requests.get("https://raw.githubusercontent.com/qweri0p/khdl/refs/heads/main/schema.json")
    schema = json.loads(r.text)

    try:
        validate(instance=cfg, schema=schema)
    except ValidationError:
        print(f"The '{cfgfile}' is incorrectly written. Make sure you comply with the JSON schema provided.", file=sys.stderr)
        exit(1)

    batchobj = []
    for item in cfg['soundtracks']:

        soundtrack = item if isinstance(item, str) else item["soundtrack"]
        if 'downloads.khinsider.com' in soundtrack:
            soundtrack = soundtrack.rsplit(str('/'), 1)[-1]

        if isinstance(item, dict):
            batchobj.append((
                soundtrack,
                item.get("format", cfg["defaultFormat"]),
                item.get("output", None),
                item.get("images", True)
            ))

        elif isinstance(item, str): # This executes if the soundtrack is noted without object
            batchobj.append((
                soundtrack,
                cfg["defaultFormat"],
                None,
                True
            ))

    return "batch", batchobj

def searchParser(args):
    finalquery = f"https://downloads.khinsider.com/search?search={' '.join(args.query)}&albumListSize=compact&type={'song' if args.song else ''}&sort=name"

    return "search", finalquery
