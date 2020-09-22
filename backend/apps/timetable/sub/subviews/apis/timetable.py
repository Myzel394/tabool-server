from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.timetable.models import TimeTable
from apps.timetable.sub.subserializers import TimeTableDetailSerializer, TimeTableListSerializer

__all__ = [
    "TimeTableViewSet"
]


class TimeTableViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return TimeTable.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return TimeTableListSerializer
        return TimeTableDetailSerializer
