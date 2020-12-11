from typing import *

import gender_guesser.detector as gender
from bs4 import BeautifulSoup, Tag
from torrequest import TorRequest

from apps.django.main.school_data.options import GenderChoices

__all__ = [
    "scrape_teachers", "TeacherInformationType"
]

DOMAIN = "rwg-neuwied.de"
URL = f"https://www.{DOMAIN}/hp/_listen/kollegiumsliste.php?access=sdfzu76234"
FIRST_NAME_INDEX = 3
LAST_NAME_INDEX = 2
SHORT_NAME_INDEX = 4

GENDER_MAP = {
    "male": GenderChoices.MALE,
    "mostly_male": GenderChoices.MALE,
    "female": GenderChoices.FEMALE,
    "mostly_female": GenderChoices.FEMALE,
    "andy": GenderChoices.UNKNOWN,
    "unknown": GenderChoices.UNKNOWN
}


class TeacherInformationType(TypedDict):
    first_name: str
    last_name: str
    short_name: str
    gender: int
    email: str


def scrape_teachers() -> List[TeacherInformationType]:
    found = []
    gender_detector = gender.Detector()
    
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
                "email": email,
                "gender": GENDER_MAP[gender_detector.get_gender(first_name, "germany")]
            })
    
    return found
