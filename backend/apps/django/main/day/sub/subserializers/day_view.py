from datetime import date, timedelta

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

__all__ = [
    "DayViewSerializer"
]

from rest_framework.exceptions import ValidationError


def get_date():
    today = date.today()
    weekday = today.weekday()
    
    if weekday >= 5:
        today += timedelta(days=7 - weekday)
    
    return today


class DayViewSerializer(serializers.Serializer):
    start_date = serializers.DateField(
        default=get_date,
        label=_("Startdatum")
    )
    
    end_date = serializers.DateField(
        default=get_date,
        label=_("Enddatum")
    )
    
    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise ValidationError(
                _("Das Startdatum ist unter dem Enddatum.")
            )
        
        return super().validate(attrs)
