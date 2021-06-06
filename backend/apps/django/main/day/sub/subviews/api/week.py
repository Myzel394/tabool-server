from datetime import date
from typing import *

from django_hint import RequestType
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from apps.django.main.event.models import Event, Exam, Modification
from apps.django.main.event.serializers import (
    DetailEventSerializer, StudentDetailExamSerializer,
    StudentDetailModificationSerializer, TeacherDetailExamSerializer, TeacherDetailModificationSerializer,
)
from apps.django.main.homework.models import Homework, Material
from apps.django.main.homework.serializers import (
    StudentDetailHomeworkSerializer, StudentDetailMaterialSerializer,
    TeacherDetailMaterialSerializer,
)
from apps.django.main.timetable.models import Timetable
from apps.django.main.timetable.serializers import StudentDetailLessonSerializer, TeacherDetailLessonSerializer
from apps.django.utils.cache import cache_for_user
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent, IsTeacher
from ....serializers import WeekViewSerializer
from ....throttles import BurstWeekViewThrottle, SustainedWeekViewThrottle

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "student_week_view", "teacher_week_view"
]

TWO_HOURS_IN_SECONDS = 60 * 60 * 2


def parse_serializer(data: dict, serializer_context: dict) -> tuple[date, date]:
    serializer = WeekViewSerializer(data=data, context=serializer_context)
    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data
    start_date = validated_data["start_date"]
    end_date = validated_data["end_date"]

    return start_date, end_date


def get_elements(user: "User", start_date: date, end_date: date) -> dict:
    start_weekday = start_date.weekday()
    end_weekday = end_date.weekday()
    start_weekday = 0 if start_weekday >= 6 else start_weekday
    weekdays = list(range(min(start_weekday, end_weekday), max(start_weekday, end_weekday) + 1))

    timetable = Timetable.objects.current(user)
    user_lessons = timetable.lessons
    lessons = user_lessons \
        .only("weekday") \
        .filter(weekday__in=weekdays)

    modifications = Modification.objects \
        .from_user(user) \
        .only("lesson_date", ) \
        .filter(lesson_date__gte=start_date, lesson_date__lte=end_date)
    materials = Material.objects \
        .from_user(user) \
        .only("lesson_date") \
        .filter(lesson_date__gte=start_date, lesson_date__lte=end_date)
    homeworks = Homework.objects \
        .from_user(user) \
        .only("lesson_date") \
        .filter(lesson_date__gte=start_date, lesson_date__lte=end_date)
    exams = Exam.objects \
        .from_user(user) \
        .only("date") \
        .filter(date__gte=start_date, date__lte=end_date)
    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_date, end_datetime__lte=end_date) \
        .distinct()

    return {
        "lessons": lessons,
        "modifications": modifications,
        "materials": materials,
        "exams": exams,
        "events": events,
        "homeworks": homeworks,
    }


@cache_for_user(TWO_HOURS_IN_SECONDS)
@api_view(["GET"])
@throttle_classes([BurstWeekViewThrottle, SustainedWeekViewThrottle])
@permission_classes([AuthenticationAndActivePermission & IsStudent])
def student_week_view(request: RequestType):
    serializer_context = {
        "request": request
    }
    start_date, end_date = parse_serializer(request.GET, serializer_context)
    user = request.user
    elements = get_elements(user, start_date=start_date, end_date=end_date)

    return Response({
        "lessons": StudentDetailLessonSerializer(
            instance=elements["lessons"],
            many=True,
            context=serializer_context
        ).data,
        "modifications": StudentDetailModificationSerializer(
            instance=elements["modifications"],
            many=True,
            context=serializer_context
        ).data,
        "materials": StudentDetailMaterialSerializer(
            instance=elements["materials"],
            many=True,
            context=serializer_context
        ).data,
        "exams": StudentDetailExamSerializer(
            instance=elements["exams"],
            many=True,
            context=serializer_context
        ).data,
        "events": DetailEventSerializer(
            instance=elements["events"],
            many=True,
            context=serializer_context
        ).data,
        "homeworks": StudentDetailHomeworkSerializer(
            instance=elements["homeworks"],
            many=True,
            context=serializer_context
        ).data,
    })


@cache_for_user(TWO_HOURS_IN_SECONDS)
@api_view(["GET"])
@throttle_classes([BurstWeekViewThrottle, SustainedWeekViewThrottle])
@permission_classes([AuthenticationAndActivePermission & IsTeacher])
def teacher_week_view(request: RequestType):
    serializer_context = {
        "request": request
    }
    start_date, end_date = parse_serializer(request.GET, serializer_context)
    user = request.user
    elements = get_elements(user, start_date=start_date, end_date=end_date)

    return Response({
        "lessons": TeacherDetailLessonSerializer(
            instance=elements["lessons"],
            many=True,
            context=serializer_context
        ).data,
        "modifications": TeacherDetailModificationSerializer(
            instance=elements["modifications"],
            many=True,
            context=serializer_context
        ).data,
        "materials": TeacherDetailMaterialSerializer(
            instance=elements["materials"],
            many=True,
            context=serializer_context
        ).data,
        "exams": TeacherDetailExamSerializer(
            instance=elements["exams"],
            many=True,
            context=serializer_context
        ).data,
        "events": DetailEventSerializer(
            instance=elements["events"],
            many=True,
            context=serializer_context
        ).data,
    })
