from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_only_future_dates(value: date):
    if value and value < date.today():
        raise ValidationError(_("Das Datum darf nicht in der Vergangenheit liegen!"))
