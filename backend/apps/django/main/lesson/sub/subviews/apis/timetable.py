from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.django.main.event.models import Event
from apps.django.main.event.sub.subserializers.event import EventDetailSerializer
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
    
    # Get data
    lessons = Lesson.objects \
        .from_user(user) \
        .only("date") \
        .filter(date__gte=start_datetime.date(), date__lte=end_datetime.date())
    events = Event.objects \
        .from_user(user) \
        .only("start_datetime", "end_datetime") \
        .filter(start_datetime__gte=start_datetime, end_datetime__lte=end_datetime)
    
    return Response({
        "lessons": LessonDetailSerializer(lessons, many=True, context=serializer_context).data,
        "events": EventDetailSerializer(events, many=True, context=serializer_context).data,
        "earliest_date_available": Lesson.objects.only("date").earliest("date").date,
        "latest_date_available": Lesson.objects.only("date").latest("date").date
    })
