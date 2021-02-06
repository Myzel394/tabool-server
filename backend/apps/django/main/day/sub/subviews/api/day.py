from datetime import date
from typing import *

from django_hint import RequestType
from rest_framework.decorators import api_view, throttle_classes

from apps.django.main.event.models import Event, Exam, Modification
from apps.django.main.event.sub.subserializers.event import DetailEventSerializer
from apps.django.main.event.sub.subserializers.exam import StudentDetailExamSerializer, TeacherDetailExamSerializer
from apps.django.main.event.sub.subserializers.modification import DetailModificationSerializer
from apps.django.main.homework.models import Homework, Material, Submission
from apps.django.main.homework.sub.subserializers.homework import (
    StudentDetailHomeworkSerializer,
    TeacherDetailHomeworkSerializer,
)
from apps.django.main.homework.sub.subserializers.material import DetailMaterialSerializer
from apps.django.main.homework.sub.subserializers.submission import DetailSubmissionSerializer
from apps.django.main.timetable.mixins import get_via_referenced_lesson_date_range
from apps.django.main.timetable.sub.subserializers.lesson import DetailLessonSerializer
from ....serializers import DayViewSerializer
from ....throttles import BurstDayViewThrottle, SustainedDayViewThrottle

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User
    from apps.django.main.timetable.models import Lesson

__all__ = [
    "student_day_view", "teacher_day_view"
]


def parse_serializer(data: dict) -> tuple[date, date]:
    serializer = DayViewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    
    validated_data = serializer.validated_data
    start_date = validated_data["start_date"]
    end_date = validated_data["end_date"]
    
    return start_date, end_date


def get_elements(user: "User", start_date: date, end_date: date) -> dict:
    lessons = Lesson.objects \
        .from_user(user) \
        .only("lesson_date") \
        .filter(lesson_date__gte=start_date, lesson_date__lte=end_date)
    modifications = get_via_referenced_lesson_date_range(Modification.objects.from_user(user), start_date, end_date)
    materials = get_via_referenced_lesson_date_range(Material.objects.from_user(user), start_date, end_date)
    submissions = get_via_referenced_lesson_date_range(Submission.objects.from_user(user), start_date, end_date)
    homeworks = get_via_referenced_lesson_date_range(Homework.objects.from_user(user), start_date, end_date)
    exams = Exam.objects \
        .from_user(user) \
        .only("date") \
        .filter(date__gte=start_date, date__lte=end_date)
    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_date, end_datetime__gte=end_date) \
        .distinct()
    
    return {
        "lessons": lessons,
        "modifications": modifications,
        "materials": materials,
        "submissions": submissions,
        "homeworks": homeworks,
        "exams": exams,
        "events": events,
    }


@api_view(["GET"])
@throttle_classes([BurstDayViewThrottle, SustainedDayViewThrottle])
def student_day_view(request: RequestType):
    start_date, end_date = parse_serializer(request.data)
    user = request.user
    serializer_context = {
        "request": request
    }
    elements = get_elements(user, start_date=start_date, end_date=end_date)
    
    return {
        "lesson": DetailLessonSerializer(instance=elements["lessons"], many=True, context=serializer_context).data,
        "modifications": DetailModificationSerializer(
            instance=elements["modifications"],
            many=True,
            context=serializer_context
        ).data,
        "materials": DetailMaterialSerializer(
            instance=elements["materials"],
            many=True,
            context=serializer_context
        ).data,
        "submissions": DetailSubmissionSerializer(
            instance=elements["submissions"],
            many=True,
            context=serializer_context
        ).data,
        "homeworks": StudentDetailHomeworkSerializer(
            instance=elements["homeworks"],
            many=True,
            context=serializer_context
        ).data,
        "exams": StudentDetailExamSerializer(instance=elements["exams"], many=True, context=serializer_context).data,
        "events": DetailEventSerializer(instance=elements["events"], many=True, context=serializer_context).data,
    }


@api_view(["GET"])
@throttle_classes([BurstDayViewThrottle, SustainedDayViewThrottle])
def teacher_day_view(request: RequestType):
    start_date, end_date = parse_serializer(request.data)
    user = request.user
    serializer_context = {
        "request": request
    }
    elements = get_elements(user, start_date=start_date, end_date=end_date)
    
    return {
        "lesson": DetailLessonSerializer(instance=elements["lessons"], many=True, context=serializer_context).data,
        "modifications": DetailModificationSerializer(
            instance=elements["modifications"],
            many=True,
            context=serializer_context
        ).data,
        "materials": DetailMaterialSerializer(
            instance=elements["materials"],
            many=True,
            context=serializer_context
        ).data,
        "submissions": DetailSubmissionSerializer(
            instance=elements["submissions"],
            many=True,
            context=serializer_context
        ).data,
        "homeworks": TeacherDetailHomeworkSerializer(
            instance=elements["homeworks"],
            many=True,
            context=serializer_context
        ).data,
        "exams": TeacherDetailExamSerializer(instance=elements["exams"], many=True, context=serializer_context).data,
        "events": DetailEventSerializer(instance=elements["events"], many=True, context=serializer_context).data,
    }
