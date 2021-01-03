import re
from datetime import date, datetime
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from constants import weekdays


def validate_place(value: str) -> None:
    if not re.match("^(([A-Z]{1,2}[0-9]?)|([0-9]){3})|([A-Z][a-z ]{62})$", value):
        raise ValidationError(
            _("Dieser Raum ist nicht gültig.")
        )


def validate_weekday_in_lesson_data_available(value: Union[date, datetime]):
    available_weekdays = [
        value
        for value, x in weekdays.ALLOWED_WEEKDAYS
    ]
    
    if value.weekday() not in available_weekdays:
        raise ValidationError(_("Dieser Wochentag ist nicht gültig."))
