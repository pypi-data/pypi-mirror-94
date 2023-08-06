# Parse markdown table into tuple of lists
# Armaan Bhojwani 2021

import sys
from bs4 import BeautifulSoup
import markdown

from .deck import Card


def md2html(file):
    """Use the markdown module to convert input to HTML"""
    try:
        return markdown.markdown(open(file, "r").read(), extensions=["tables"])
    except FileNotFoundError:
        raise Exception(
            f'lightcards: "{file}": No such file or directory'
        ) from None


def parse_html(html):
    """Use BeautifulSoup to parse the HTML"""

    def clean_text(inp):
        return inp.get_text().rstrip()

    soup = BeautifulSoup(html, "html.parser").find("table")
    outp = []

    try:
        for x in soup.find_all("tr"):
            outp.append(Card(tuple([clean_text(y) for y in x.find_all("td")])))
    except AttributeError:
        raise Exception("lightcards: No table found") from None

    ths = soup.find_all("th")
    if len(ths) != 2:
        raise Exception("lightcards: Headings malformed")

    # Return a tuple of nested lists
    return ([clean_text(x) for x in ths], outp[1:])


def main(file):
    return parse_html(md2html(file))


if __name__ == "__main__":
    print(main(sys.argv[1]))
