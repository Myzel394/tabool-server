from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.django.main.event.models import Event, Exam, Modification
from apps.django.main.event.sub.subserializers.event.detail import DetailEventSerializer
from apps.django.main.event.sub.subserializers.exam.detail import DetailExamSerializer
from apps.django.main.event.sub.subserializers.modification.detail import DetailModificationSerializer
from apps.django.main.homework.models import Homework, Material
from apps.django.main.homework.sub.subserializers.homework.detail import DetailHomeworkSerializer
from apps.django.main.homework.sub.subserializers.material.detail import DetailMaterialSerializer
from apps.django.utils.cache import cache_for_user
from ....models import Lesson
from ....serializers import RelatedDetailLessonSerializer, TimetableSerializer

__all__ = [
    "timetable"
]

FOUR_MINUTES_IN_SECONDS = 60 * 4


@cache_for_user(FOUR_MINUTES_IN_SECONDS)
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
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Get data
    user_lessons = Lesson.objects \
        .from_user(user)
    lessons = user_lessons \
        .only("date") \
        .filter(date__gte=start_datetime.date(), date__lte=end_datetime.date())
    course_ids = lessons.values_list("course__id", flat=True).distinct()
    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_datetime, end_datetime__lte=end_datetime)
    exams = Exam.objects \
        .only("course", "targeted_date") \
        .filter(course__id__in=course_ids, targeted_date__gte=start_datetime.date(),
                targeted_date__lte=end_datetime.date()) \
        .distinct()
    materials = Material.objects \
        .only("lesson") \
        .filter(lesson__in=lessons)
    homeworks = Homework.objects \
        .only("lesson") \
        .filter(lesson__in=lessons)
    modifications = Modification.objects \
        .only("lesson") \
        .filter(lesson__in=lessons)
    
    return Response({
        "lessons": RelatedDetailLessonSerializer(lessons, many=True, context=serializer_context).data,
        "events": DetailEventSerializer(events, many=True, context=serializer).data,
        "exams": DetailExamSerializer(exams, many=True, context=serializer_context).data,
        "materials": DetailMaterialSerializer(materials, many=True, context=serializer_context).data,
        "homeworks": DetailHomeworkSerializer(homeworks, many=True, context=serializer_context).data,
        "modifications": DetailModificationSerializer(modifications, many=True, context=serializer_context).data,
        "earliest_date_available": user_lessons.only("date").earliest("date").date,
        "latest_date_available": user_lessons.only("date").latest("date").date
    })
