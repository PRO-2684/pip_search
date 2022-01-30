from requests import get
from bs4 import BeautifulSoup
from sys import argv
from rich.console import Console
from rich.table import Table

console = Console()
if len(argv) != 2:
    console.print("Usage: pip_search.py <package name>", highlight=False)
    exit(1)
r = get("https://pypi.org/search/?q=" + argv[1])
soup = BeautifulSoup(r.text, "html.parser")
result = soup.find_all("a", class_="package-snippet")
info = dict()
for i in result:
    info[i.find("span", class_="package-snippet__name").text.strip()] = {
        "version": i.find("span", class_="package-snippet__version").text.strip(),
        "release": i.find("span", class_="package-snippet__released").text.strip(),
        "description": i.find("p", class_="package-snippet__description").text.strip(),
    }
show = Table(
    "Name",
    "Latest Version",
    "Release Date",
    "Description",
    title=f"Search results for {argv[1]}",
)
for name, value in info.items():
    description = value["description"]
    if not description:
        description = "[italic]No description available."
    show.add_row(name, value["version"], value["release"], description)
console.print(show)
