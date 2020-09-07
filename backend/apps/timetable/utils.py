from datetime import date
from typing import *

from django.utils.translation import gettext_lazy as _


def create_designation_from_date(
        targeted_date: Optional[date] = None,
        half_year_month: int = 6
):
    targeted_date = targeted_date or date.today()
    
    if targeted_date.month <= half_year_month:
        return _("1. Halbjahr {}").format(targeted_date.year)
    return _("2. Halbjahr {}").format(targeted_date.year)
