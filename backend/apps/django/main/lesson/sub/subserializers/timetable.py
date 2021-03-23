from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

__all__ = [
    "TimetableSerializer"
]


class TimetableSerializer(serializers.Serializer):
    MAX_DAYS_DIFF = 7 * 6  # 6 Weeks
    
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        start_datetime = attrs["start_datetime"]
        end_datetime = attrs["end_datetime"]
        
        if end_datetime <= start_datetime:
            raise ValidationError({
                "end_datetime": _("Das Enddatum muss größer als das Startdatum sein")
            })
        
        diff: timedelta = end_datetime - start_datetime
        
        if diff.days > self.MAX_DAYS_DIFF:
            raise ValidationError({
                "end_datetime": _(
                    "Das Enddatum kann höchstens {max_days_diff} Tage über dem Startdatum liegen."
                ).format(max_days_diff=self.MAX_DAYS_DIFF)
            })
        
        return data
