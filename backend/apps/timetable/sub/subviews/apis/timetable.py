from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.timetable.models import Timetable
from apps.timetable.sub.subserializers import TimetableDetailSerializer, TimetableListSerializer

__all__ = [
    "TimetableViewSet"
]


class TimetableViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return Timetable.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return TimetableListSerializer
        return TimetableDetailSerializer
