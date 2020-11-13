from datetime import date
from typing import *

from . import constants

if TYPE_CHECKING:
    pass

__all__ = [
    "get_school_starts_date_for_year"
]


def get_school_starts_date_for_year(year: Optional[int]) -> date:
    year = year or date.today().year
    
    return date(
        year,
        constants.SCHOOL_YEAR_START_DATE.month,
        constants.SCHOOL_YEAR_START_DATE.day
    )
