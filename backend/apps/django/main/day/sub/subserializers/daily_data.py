from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.main.timetable.models import Lesson
from apps.django.utils.serializers import ValidationSerializer
from ...utils import get_date

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "DailyDataViewSerializer"
]


class DailyDataViewSerializer(ValidationSerializer):
    date = serializers.DateField(default=get_date)
    max_future_days = serializers.IntegerField(min_value=0, max_value=30, default=5)
    
    @staticmethod
    def get_weekdays(user: "User") -> set[int]:
        available_weekdays = Lesson.objects \
            .from_user(user) \
            .only("weekday") \
            .values_list("weekday", flat=True)
        
        return set(available_weekdays)
    
    def validate_date(self, value: date):
        user = self.context["request"].user
        available_weekdays = self.get_weekdays(user)
        weekday = value.weekday()
        
        if weekday not in available_weekdays:
            raise ValidationError(_("Ungültiger Wochentag"))
        
        return value
