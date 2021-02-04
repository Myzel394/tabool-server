from datetime import date, datetime
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from constants import weekdays


def validate_weekday_in_lesson_data_available(value: Union[date, datetime]):
    available_weekdays = [
        value
        for value, x in weekdays.ALLOWED_WEEKDAYS
    ]
    
    if value.weekday() not in available_weekdays:
        raise ValidationError(_("Dieser Wochentag ist nicht gültig."))
