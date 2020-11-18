from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.django.main.event.models import Event, Modification
from apps.django.main.event.sub.subserializers.event import EventDetailSerializer
from apps.django.main.event.sub.subserializers.modification import ModificationDetailSerializer
from apps.django.main.homework.models import Homework, Material
from apps.django.main.homework.sub.subserializers.homework import HomeworkListSerializer
from apps.django.main.homework.sub.subserializers.material import MaterialListSerializer
from ....models import Lesson
from ....serializers import LessonDetailSerializer, TimetableSerializer

__all__ = [
    "timetable"
]


@api_view(["GET"])
def timetable(request):
    user = request.user
    serializer_context = {
        "request": request
    }
    
    # Validation
    serializer = TimetableSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    
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
        .filter(lesson__id__in=lessons_ids)
    materials = Material.objects \
        .only("lesson") \
        .filter(lesson__id__in=lessons_ids)
    
    return Response({
        "lessons": LessonDetailSerializer(lessons, many=True, context=serializer_context).data,
        "modifications": ModificationDetailSerializer(modifications, many=True, context=serializer_context).data,
        "events": EventDetailSerializer(events, many=True, context=serializer_context).data,
        "homeworks": HomeworkListSerializer(homeworks, many=True, context=serializer_context).data,
        "materials": MaterialListSerializer(materials, many=True, context=serializer_context).data
    })
