from prettytable import PrettyTable
from bs4 import BeautifulSoup
import requests, sys, json
from pathlib import Path

BASEJSON = {
    "$schema": "https://raw.githubusercontent.com/qwerinope/khidl/refs/heads/main/schema.json",
    "defaultFormat": "mp3",
    "soundtracks": []
}

class SearchParsingError(Exception):
    """This should NEVER EVER be triggered. If khinsider's website changes this might get set off but that's very unlikely"""

class SearchNoResults(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def search(url, jsonpath):
    if json:
        jsonfile = Path(jsonpath)
        if jsonfile.exists():
            print(f"Cannot write to {jsonfile} because it already exists", file=sys.stderr)
            sys.exit(1)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Encoding": "identity",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Site":"same-site"}

    r = requests.get(url, headers=headers)
    parser = BeautifulSoup(r.text, 'html.parser')
    albumlist = parser.select_one('.albumList')

    if not albumlist:
        raise SearchNoResults

    table = PrettyTable()
    table.align = 'l' # Table align left
    table.field_names = ["Soundtrack", "ID", "Year"]

    for index, ost in enumerate(albumlist.find_all('tr')):
        if index == 0:
            continue

        anchors = ost.find_all('a')
        goodanchor = anchors[1]
        ostid = goodanchor.get('href').rsplit('/', 1)[-1]

        if jsonpath:
            BASEJSON["soundtracks"].append(ostid)
        else:
            table.add_row([goodanchor.get_text(), ostid, ost.select_one("td:last-of-type").get_text()])

    if not jsonpath:
        print(table)
    else:
        jsonfile.write_text(json.dumps(BASEJSON, indent=2))
        print(f"Successfully written {len(BASEJSON['soundtracks'])} soundtracks to {jsonfile}")
