from datetime import date, datetime, time, timedelta
from typing import *

from django.db.models import Q
from django_hint import RequestType
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from apps.django.main.event.models import Event, Modification
from apps.django.main.event.sub.subserializers.event import DetailEventSerializer
from apps.django.main.event.sub.subserializers.modification import TeacherDetailModificationSerializer
from apps.django.main.homework.models import Homework, Submission, Classbook, Material
from apps.django.main.homework.sub.subserializers.classbook import TeacherDetailClassbookSerializer
from apps.django.main.homework.sub.subserializers.homework import TeacherDetailHomeworkSerializer
from apps.django.main.homework.sub.subserializers.material import TeacherDetailMaterialSerializer
from apps.django.main.homework.sub.subserializers.submission import TeacherDetailSubmissionSerializer
from apps.django.main.timetable.models import Lesson
from apps.django.main.timetable.sub.subserializers.lesson import TeacherDetailLessonSerializer
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacher
from ...subthrottles.daily_data import SustainedDailyDataViewThrottle, BurstDailyDataViewThrottle
from ....serializers import DailyDataViewSerializer

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User

__all__ = [
    "teacher_daily_data_view"
]


def parse_serializer(data: dict, serializer_context: dict) -> tuple[date, int]:
    serializer = DailyDataViewSerializer(data=data, context=serializer_context)
    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data
    targeted_date = validated_data["date"]
    max_future_days = validated_data["max_future_days"]

    return targeted_date, max_future_days


# Timetable + Modifications
# Homeworks
# Submissions
# Video conferences
# Materials
# Events
def get_elements(user: "User", targeted_date: date, max_future_days: int):
    start_date = datetime.combine(targeted_date, time.min)
    end_date = targeted_date + timedelta(days=max_future_days)
    end_date = datetime.combine(end_date, time.max)

    # Only fetch lessons for this date
    weekday = targeted_date.weekday()
    user_lessons = Lesson.objects.from_user(user)
    date_lessons = user_lessons \
        .only("weekday") \
        .filter(weekday=weekday)

    # Based on `date_lessons`
    modifications = Modification.objects \
        .from_user(user) \
        .only("lesson", "lesson_date") \
        .filter(lesson__in=date_lessons, lesson_date=targeted_date)

    # Based on `max_future_days`
    homework_date_filter = Q(lesson__in=user_lessons, lesson_date=targeted_date) | \
                           Q(due_date__gte=start_date, due_date__lte=end_date) | \
                           Q(due_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
    homeworks = Homework.objects \
        .from_user(user) \
        .only("due_date", "lesson") \
        .filter(homework_date_filter)

    submissions = Submission.objects \
        .from_user(user) \
        .only("lesson", "lesson_date") \
        .filter(lesson__in=user_lessons) \
        .filter(lesson_date__gte=start_date, lesson_date__lte=end_date)

    classbook_with_video_conferences = Classbook.objects \
        .from_user(user) \
        .only("video_conference_link", "lesson_date") \
        .filter(video_conference_link__isnull=False) \
        .filter(lesson_date__gte=start_date, lesson_date__lte=end_date)

    material_date_filter = Q(lesson__in=user_lessons, lesson_date=targeted_date) | \
                           Q(publish_datetime__gte=start_date, publish_datetime__lte=end_date)
    materials = Material.objects \
        .from_user(user) \
        .only("lesson", "lesson_date", "publish_datetime") \
        .filter(material_date_filter)

    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_date, start_datetime__lte=end_date) \
        .filter(end_datetime__gte=start_date, end_datetime__lte=end_date)

    return {
        "lessons": date_lessons,
        "modifications": modifications,
        "homeworks": homeworks,
        "submissions": submissions,
        "classbook_with_video_conferences": classbook_with_video_conferences,
        "materials": materials,
        "events": events
    }


@api_view(["GET"])
@permission_classes([AuthenticationAndActivePermission & IsTeacher])
@throttle_classes([BurstDailyDataViewThrottle, SustainedDailyDataViewThrottle])
def teacher_daily_data_view(request: RequestType):
    serializer_context = {
        "request": request
    }
    targeted_date, max_future_days = parse_serializer(request.GET, serializer_context)
    user = request.user
    elements = get_elements(user, targeted_date, max_future_days)

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
        "homeworks": TeacherDetailHomeworkSerializer(
            instance=elements["homeworks"],
            many=True,
            context=serializer_context
        ).data,
        "submissions": TeacherDetailSubmissionSerializer(
            instance=elements["submissions"],
            many=True,
            context=serializer_context
        ).data,
        "classbook_with_video_conferences": TeacherDetailClassbookSerializer(
            instance=elements["classbook_with_video_conferences"],
            many=True,
            context=serializer_context,
        ).data,
        "materials": TeacherDetailMaterialSerializer(
            instance=elements["materials"],
            many=True,
            context=serializer_context
        ).data,
        "events": DetailEventSerializer(
            instance=elements["events"],
            many=True,
            context=serializer_context
        ).data
    })
