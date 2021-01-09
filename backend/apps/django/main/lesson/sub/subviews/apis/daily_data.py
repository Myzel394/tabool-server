from datetime import date, datetime, time, timedelta

from django.utils.translation import gettext_lazy as _
from django_hint import RequestType
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.django.main.event.models import Event, Exam, Modification
from apps.django.main.event.sub.subserializers.event import EventDetailSerializer
from apps.django.main.event.sub.subserializers.exam import ExamDetailSerializer
from apps.django.main.event.sub.subserializers.modification import ModificationDetailSerializer
from apps.django.main.homework.models import Homework
from apps.django.main.homework.sub.subserializers.homework import HomeworkDetailSerializer
from ....models import Lesson
from ....serializers import DailyDataSerializer, LessonDetailSerializer


@api_view(["GET"])
def daily_data(request: RequestType):
    # Validation
    serializer = DailyDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    # Variables
    user = request.user
    serializer_context = {
        "request": request
    }
    data = serializer.validated_data
    targeted_date: date = data["date"]
    max_future_days: int = data["max_future_days"]
    
    # Empty guard
    if Lesson.objects.count() == 0:
        return Response({
            "detail": _("Der Stundenplan wurde noch nicht geladen.")
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Get data
    lessons = Lesson.objects \
        .from_user(user) \
        .only("date") \
        .filter(date=targeted_date)
    course_ids = lessons.values_list("lesson_data__course", flat=True).distinct()
    modifications = Modification.objects \
        .only("lesson") \
        .filter(lesson__in=lessons) \
        .distinct()
    homeworks = Homework.objects \
        .only("lesson") \
        .filter(lesson__in=lessons)
    exams = Exam.objects \
        .only("course", "targeted_date") \
        .filter(course__id__in=course_ids,
                targeted_date__gte=targeted_date,
                targeted_date__lte=targeted_date + timedelta(days=max_future_days)) \
        .distinct()
    events = Event.objects \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=datetime.combine(targeted_date, time.min),
                end_datetime__lte=datetime.combine(targeted_date + timedelta(days=max_future_days), time.max)) \
        .distinct()
    video_conference_lessons = Lesson.objects \
        .from_user(user) \
        .only("video_conference_link", "date") \
        .filter(video_conference_link__isnull=False,
                date__gte=targeted_date,
                date__lte=targeted_date + timedelta(days=max_future_days)) \
        .distinct()
    
    return Response({
        "lessons": LessonDetailSerializer(lessons, many=True, context=serializer_context).data,
        "modifications": ModificationDetailSerializer(modifications, many=True, context=serializer_context).data,
        "homeworks": HomeworkDetailSerializer(homeworks, many=True, context=serializer_context).data,
        "exams": ExamDetailSerializer(exams, many=True, context=serializer_context).data,
        "events": EventDetailSerializer(events, many=True, context=serializer).data,
        "video_conference_lessons": LessonDetailSerializer(
            video_conference_lessons, many=True, context=serializer_context
        ).data
    })
