import calendar

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.django.main.timetable.public.serializer_fields.lesson import LessonField

__all__ = [
    "LessonViewSerializer"
]


class LessonViewSerializer(serializers.Serializer):
    lesson = LessonField()
    lesson_date = serializers.DateField()
    
    def validate(self, attrs):
        if attrs["lesson_date"].weekday() != (required_weekday := attrs["lesson"].weekday()):
            weekdays = list(calendar.day_name)
            
            raise ValidationError({
                "lesson_date": _("Das Datum ist nicht gültig. Es muss ein {weekday} sein.").format(
                    weekday=weekdays[required_weekday]
                )
            })
        
        return super().validate(attrs)
