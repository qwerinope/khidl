from prettytable import PrettyTable
from bs4 import BeautifulSoup
import requests

class SearchParsingError(Exception):
    """This should NEVER EVER be triggered. If khinsider's website changes this might get set off but that's very unlikely"""

class SearchNoResults(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def search(url):
    r = requests.get(url)
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

        table.add_row([goodanchor.get_text(), goodanchor.get('href').rsplit(str('/'),1)[-1], ost.select_one("td:last-of-type").get_text()])

    print(table)
