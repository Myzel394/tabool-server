from datetime import date, datetime, time, timedelta
from typing import *

from django.db.models import Q
from django_hint import RequestType
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from apps.django.main.event.models import Event, Exam, Modification
from apps.django.main.event.sub.subserializers.event import DetailEventSerializer
from apps.django.main.event.sub.subserializers.exam import StudentDetailExamSerializer
from apps.django.main.event.sub.subserializers.modification import StudentDetailModificationSerializer
from apps.django.main.homework.models import Classbook, Homework, Material
from apps.django.main.homework.sub.subserializers.classbook import StudentDetailClassbookSerializer
from apps.django.main.homework.sub.subserializers.homework import StudentDetailHomeworkSerializer
from apps.django.main.homework.sub.subserializers.material import StudentDetailMaterialSerializer
from apps.django.main.timetable.models import Timetable
from apps.django.main.timetable.sub.subserializers.lesson import StudentDetailLessonSerializer
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent
from ....serializers import DailyDataViewSerializer
from ....throttles import BurstDailyDataViewThrottle, SustainedDailyDataViewThrottle

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "student_daily_data_view"
]


def parse_serializer(data: dict, serializer_context: dict) -> tuple[date, int]:
    serializer = DailyDataViewSerializer(data=data, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    
    validated_data = serializer.validated_data
    targeted_date = validated_data["date"]
    max_future_days = validated_data["max_future_days"]
    
    return targeted_date, max_future_days


def get_elements(user: "User", targeted_date: date, max_future_days: int):
    start_date = datetime.combine(targeted_date, time.min)
    end_date = targeted_date + timedelta(days=max_future_days)
    end_date = datetime.combine(end_date, time.max)
    
    timetable = Timetable.objects.current(user)
    user_lessons = timetable.lessons
    # Based on the courses we can fetch the other elements. If we would use `lessons`, we would only get elements
    # from `targeted_date`. We also want to fetch elements from the future based on `max_future_days`.
    course_ids = set(user_lessons.values_list("course", flat=True))
    # Only fetch lessons for this date
    weekday = targeted_date.weekday()
    lessons = user_lessons \
        .only("weekday") \
        .filter(weekday=weekday)
    
    # These are based on `lessons` we don't need to fetch any from the future.
    modifications = Modification.objects \
        .from_user(user) \
        .only("lesson", "lesson_date") \
        .filter(lesson__in=lessons, lesson_date=targeted_date)
    materials = Material.objects \
        .from_user(user) \
        .only("lesson", "lesson_date") \
        .filter(lesson__in=lessons, lesson_date=targeted_date)
    
    # These are based on `max_future_days`
    exams = Exam.objects \
        .from_user(user) \
        .only("course", "date") \
        .filter(course__in=course_ids) \
        .filter(date__gte=start_date, date__lte=end_date)
    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_date, start_datetime__lte=end_date) \
        .filter(end_datetime__gte=start_date, end_datetime__lte=end_date)
    
    # These are based on both variables
    homework_not_completed_filter = Q(userhomeworkrelation__completed=False) | Q(userhomeworkrelation__isnull=True)
    homework_date_filter = Q(lesson__in=lessons, lesson_date=targeted_date) | \
                           Q(due_date__gte=start_date, due_date__lte=end_date) | \
                           Q(due_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
    homeworks = Homework.objects \
        .from_user(user) \
        .only("due_date", "lesson") \
        .filter(homework_not_completed_filter) \
        .filter(homework_date_filter) \
        .distinct()
    classbook_with_video_conferences = Classbook.objects \
        .from_user(user) \
        .only("video_conference_link", "lesson_date") \
        .filter(video_conference_link__isnull=False) \
        .filter(lesson_date__gte=start_date, lesson_date__lte=end_date)
    
    return {
        "lessons": lessons,
        "modifications": modifications,
        "materials": materials,
        "exams": exams,
        "events": events,
        "homeworks": homeworks,
        "classbook_with_video_conferences": classbook_with_video_conferences
    }


@api_view(["GET"])
@permission_classes([AuthenticationAndActivePermission & IsStudent])
@throttle_classes([BurstDailyDataViewThrottle, SustainedDailyDataViewThrottle])
def student_daily_data_view(request: RequestType):
    serializer_context = {
        "request": request
    }
    targeted_date, max_future_days = parse_serializer(request.GET, serializer_context)
    user = request.user
    elements = get_elements(user, targeted_date, max_future_days)
    
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
        "classbook_with_video_conferences": StudentDetailClassbookSerializer(
            instance=elements["classbook_with_video_conferences"],
            many=True,
            context=serializer_context
        ).data
    })
