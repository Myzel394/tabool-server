from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...utils import get_date

__all__ = [
    "WeekViewSerializer"
]

MAX_DAYS = 7 * 5  # 5 weeks


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
        start_date = attrs["start_date"]
        end_date = attrs["end_date"]
        
        if end_date < start_date:
            raise ValidationError(
                _("Das Enddatum muss über dem Startdatum liegen.")
            )
        
        diff = end_date - start_date
        
        if diff.days > MAX_DAYS:
            raise ValidationError(
                _(f"Du kannst höchstens {MAX_DAYS} Tage vorspulen.")
            )
        
        return super().validate(attrs)
