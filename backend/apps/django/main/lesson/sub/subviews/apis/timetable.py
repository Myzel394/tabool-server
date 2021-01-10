from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.django.main.event.models import Event, Exam
from apps.django.main.event.sub.subserializers.event import EventDetailSerializer
from apps.django.main.event.sub.subserializers.exam import ExamDetailSerializer
from ....models import Lesson
from ....serializers import LessonDetailSerializer, TimetableSerializer

__all__ = [
    "timetable"
]


@api_view(["GET"])
def timetable(request):
    # Validation
    serializer = TimetableSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    
    # Variables
    user = request.user
    serializer_context = {
        "request": request
    }
    data = serializer.validated_data
    start_datetime: datetime = data["start_datetime"]
    end_datetime: datetime = data["end_datetime"]
    
    # Empty guard
    if Lesson.objects.count() == 0:
        return Response({
            "detail": _("Der Stundenplan wurde noch nicht geladen.")
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    # Get data
    user_lessons = Lesson.objects \
        .from_user(user)
    lessons = user_lessons \
        .only("date") \
        .filter(date__gte=start_datetime.date(), date__lte=end_datetime.date())
    course_ids = lessons.values_list("lesson_data__course__id", flat=True).distinct()
    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_datetime, end_datetime__lte=end_datetime)
    exams = Exam.objects \
        .only("course", "targeted_date") \
        .filter(course__id__in=course_ids, targeted_date__gte=start_datetime.date(),
                targeted_date__lte=end_datetime.date()) \
        .distinct()
    
    return Response({
        "lessons": LessonDetailSerializer(lessons, many=True, context=serializer_context).data,
        "events": EventDetailSerializer(events, many=True, context=serializer_context).data,
        "exams": ExamDetailSerializer(exams, many=True, context=serializer_context).data,
        "earliest_date_available": user_lessons.only("date").earliest("date").date,
        "latest_date_available": user_lessons.only("date").latest("date").date
    })
