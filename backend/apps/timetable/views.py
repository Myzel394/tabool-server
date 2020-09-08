from rest_framework import viewsets

from .models import Lesson, TimeTable
from .serializers import TimeTableSerializer

__all__ = [
    "TimeTableViewSet"
]


class TimeTableViewSet(viewsets.ModelViewSet):
    serializer_class = TimeTableSerializer
    queryset = TimeTable.objects.all()
    
    def get_queryset(self):
        return Lesson.objects.all()
