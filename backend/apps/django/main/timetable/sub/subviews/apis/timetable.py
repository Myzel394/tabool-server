from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
        current_timetable = Timetable.objects.current(self.request.user)
        serializer = self.serializer_class(current_timetable, context={
            "request": self.request
        })
        
        return Response(serializer.data)
