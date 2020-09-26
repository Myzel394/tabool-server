import re
from datetime import date, datetime
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from constants import weekdays


def validate_place(value: str) -> None:
    if not re.match("^(([A-Z]*[0-9]+)|([a-zA-Z]+))$", value):
        raise ValidationError(
            _('Der Raum "{}" ist nicht gültig.').format(value)
        )


def validate_weekday_in_lesson_data_available(value: Union[date, datetime]):
    available_weekdays = [
        x[0]
        for x in weekdays.ALLOWED_WEEKDAYS
    ]
    
    if (given_value := value).weekday() not in (available_values := available_weekdays):
        raise ValidationError(_("Dieser Wochentag ist nicht gültig!").format(
            given_value=given_value,
            available_values=available_values
        ))
