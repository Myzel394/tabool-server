from rest_framework import viewsets

from ....models import Timetable
from ....serializers import DetailTimetableSerializer

__all__ = [
    "TimetableViewSet"
]


class TimetableViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.RetrieveModelMixin
):
    serializer_class = DetailTimetableSerializer
    
    def get_queryset(self):
        return Timetable.objects.from_user(self.request.user)
