from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.main.timetable.models import Lesson
from ...utils import get_date

__all__ = [
    "DailyDataViewSerializer"
]


class DailyDataViewSerializer(serializers.Serializer):
    date = serializers.DateField(default=get_date)
    max_future_days = serializers.IntegerField(min_value=0, max_value=30, default=5)
    
    def validate_date(self, value: date):
        user = self.context["request"].user
        available_weekdays = set(Lesson.objects.from_user(user).values_list("weekday", flat=True))
        weekday = value.weekday()
        
        if weekday not in available_weekdays:
            raise ValidationError(_("Ungültiger Wochentag"))
        
        return value
