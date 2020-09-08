from rest_framework import viewsets

from .models import Lesson
from .serializers import TimeTableSerializer

__all__ = [
    "LessonViewSet"
]


class TimeTableViewSet(viewsets.ModelViewSet):
    serializer_class = TimeTableSerializer
    queryset = TimeTable.objects.all()
    
    def get_queryset(self):
        return Lesson.objects.all()
