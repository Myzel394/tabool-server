from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.django.main.event.models import Event, Modification
from apps.django.main.event.sub.subserializers.event import EventDetailSerializer
from apps.django.main.event.sub.subserializers.modification import ModificationDetailSerializer
from apps.django.main.homework.models import Homework, Material
from apps.django.main.homework.serializers import HomeworkDetailEndpointSerializer, MaterialListSerializer
from ....models import Lesson
from ....serializers import LessonTimetableSerializer, TimetableSerializer

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
    
    # Get data
    lessons = Lesson.objects \
        .from_user(user) \
        .only("date") \
        .filter(date__gte=start_datetime.date(), date__lte=end_datetime.date())
    lessons_ids = lessons.values_list("id", flat=True).distinct()
    modifications = Modification.objects \
        .from_user(user) \
        .only("lesson") \
        .filter(lesson__id__in=lessons_ids)
    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_datetime, end_datetime__lte=end_datetime)
    homeworks = Homework.objects \
        .from_user(user) \
        .only("lesson") \
        .filter(lesson__id__in=lessons_ids)
    materials = Material.objects \
        .only("lesson") \
        .filter(lesson__id__in=lessons_ids)
    
    return Response({
        "lessons": LessonTimetableSerializer(lessons, many=True, context=serializer_context).data,
        "modifications": ModificationDetailSerializer(modifications, many=True, context=serializer_context).data,
        "events": EventDetailSerializer(events, many=True, context=serializer_context).data,
        "homeworks": HomeworkDetailEndpointSerializer(homeworks, many=True, context=serializer_context).data,
        "materials": MaterialListSerializer(materials, many=True, context=serializer_context).data,
        "earliest_date_available": Lesson.objects.only("date").earliest("date").date,
        "latest_date_available": Lesson.objects.only("date").latest("date").date
    })
