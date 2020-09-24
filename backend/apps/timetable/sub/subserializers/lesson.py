from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

__all__ = [
    "LessonAccessSerializer"
]


class LessonAccessSerializer(serializers.Serializer):
    MAX_DIFF = 5  # 5 Days
    
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    
    def validate(self, attrs: dict):
        start_date = attrs["start_date"]
        end_date = attrs["end_date"]
        
        difference = end_date - start_date
        
        if not (0 <= difference.days <= self.MAX_DIFF):
            raise ValidationError(
                _("Es können nicht mehr Date als für {max_diff} Tage gesendet werden!").format(
                    max_diff=self.MAX_DIFF
                )
            )
        
        return super().validate(attrs)
