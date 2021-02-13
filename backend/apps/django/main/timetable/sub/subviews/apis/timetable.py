from datetime import date

from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action

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
    
    @action(["GET"], detail=False)
    def current(self, request: RequestType):
        today = date.today()
        timetables = self \
            .get_queryset() \
            .only("start_date", "end_date") \
            .filter(start_date__lte=today, end_date__gte=today)
        current_timetable = timetables.first()
        serializer = self.serializer_class(current_timetable)
        
        return serializer
