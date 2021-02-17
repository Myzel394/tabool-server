from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...utils import get_date

__all__ = [
    "WeekViewSerializer"
]


class WeekViewSerializer(serializers.Serializer):
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
                _("Das Enddatum muss über dem Startdatum liegen.")
            )
        
        return super().validate(attrs)
