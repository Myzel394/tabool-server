from rest_framework import serializers

from apps.django.main.timetable.models import Timetable
from ....models import Course

__all__ = [
    "BaseCourseSerializer", "ParticipantsCountMixin", "WeekdaysMixin"
]


class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course


class ParticipantsCountMixin(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()
    
    @staticmethod
    def get_participants_count(obj: Course) -> int:
        return obj.participants.all().count()


class WeekdaysMixin(serializers.ModelSerializer):
    weekdays = serializers.SerializerMethodField()
    
    def get_weekdays(self, obj: Course) -> list[int]:
        user = self.context["request"].user
        timetable = Timetable.objects.current(user)
        lessons = timetable.lessons
        course_lessons = lessons.only("course").filter(course=obj)
        weekdays = set(course_lessons.values_list("weekday", flat=True))
        
        return list(weekdays)
