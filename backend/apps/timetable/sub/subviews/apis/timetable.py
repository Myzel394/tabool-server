from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.timetable.models import TimeTable
from apps.timetable.serializers import TimeTableSerializer

__all__ = [
    "TimeTableViewSet"
]


class TimeTableViewSet(viewsets.ModelViewSet):
    serializer_class = TimeTableSerializer
    queryset = TimeTable.objects.all()
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return TimeTable.objects.all()
