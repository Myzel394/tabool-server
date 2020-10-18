from datetime import date, datetime
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_only_future_days(value: Union[datetime, date]):
    if isinstance(value, datetime):
        if value < datetime.now():
            raise ValidationError(_("Es sind nur zukünftige Daten erlaubt!"))
    elif isinstance(value, date):
        if value < date.today():
            raise ValidationError(_("Es sind nur zukünftige Daten erlaubt!"))