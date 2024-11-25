from prettytable import PrettyTable
from bs4 import BeautifulSoup
import requests

class SearchParsingError(Exception):
    pass

def search(url):
    r = requests.get(url)
    parser = BeautifulSoup(r.text, 'html.parser')
    albumlist = parser.select_one('.albumList')

    if not albumlist:
        raise SearchParsingError

    table = PrettyTable()
    table.align = 'l' # Table align left
    table.field_names = ["Soundtrack", "ID", "Year"]

    for index, ost in enumerate(parser.find_all('tr')):
        if index == 0:
            continue

        anchors = ost.find_all('a')
        goodanchor = anchors[1]

        table.add_row([goodanchor.get_text(), goodanchor.get('href').rsplit(str('/'),1)[-1], ost.select_one("td:last-of-type").get_text()])

    print(table)
