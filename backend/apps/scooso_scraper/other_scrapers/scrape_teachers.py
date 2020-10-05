from typing import *

from bs4 import BeautifulSoup, Tag
from torrequest import TorRequest

__all__ = [
    "scrape_teachers", "TeacherInformationType"
]

DOMAIN = "rwg-neuwied.de"
URL = f"https://www.{DOMAIN}/hp/_listen/kollegiumsliste.php?access=sdfzu76234"
FIRST_NAME_INDEX = 3
LAST_NAME_INDEX = 2
SHORT_NAME_INDEX = 4


class TeacherInformationType(TypedDict):
    first_name: str
    last_name: str
    short_name: str
    email: str


def scrape_teachers() -> List[TeacherInformationType]:
    found = []
    
    with TorRequest() as tr:
        response = tr.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        for row in soup.select("tbody tr"):  # type: Tag
            first_name = row.select_one(f"td:nth-child({FIRST_NAME_INDEX})").get_text().strip()
            last_name = row.select_one(f"td:nth-child({LAST_NAME_INDEX})").get_text().strip()
            short_name = row.select_one(f"td:nth-child({SHORT_NAME_INDEX})").get_text().strip()
            email = row.select_one("a[href^='mailto']")["href"].strip().lower()
            
            found.append({
                "first_name": first_name,
                "last_name": last_name,
                "short_name": short_name,
                "email": email
            })
    
    return found
