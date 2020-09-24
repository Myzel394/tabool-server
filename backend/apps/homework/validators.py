from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_only_future_days(value: datetime):
    if isinstance(value, datetime):
        if datetime.now() >= value:
            raise ValidationError(_("Es sind nur zukünftige Daten erlaubt!"))
    elif isinstance(value, date):
        if date.today() >= value:
            raise ValidationError(_("Es sind nur zukünftige Daten erlaubt!"))
