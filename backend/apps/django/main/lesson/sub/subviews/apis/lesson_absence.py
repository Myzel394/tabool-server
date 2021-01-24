from rest_framework import viewsets

from ....models import LessonAbsence
from ....serializers import CreateLessonAbsenceSerializer, DetailLessonAbsenceSerializer, UpdateLessonAbsenceSerializer

__all__ = [
    "LessonAbsenceView"
]

# TODO: Apply this scheme to all views!
SERIALIZER_ACTION_MAP = {
    "list": DetailLessonAbsenceSerializer,
    "retrieve": DetailLessonAbsenceSerializer,
    "create": CreateLessonAbsenceSerializer,
    "update": UpdateLessonAbsenceSerializer,
    "partial_update": UpdateLessonAbsenceSerializer,
    "destroy": None
}


class LessonAbsenceView(viewsets.ModelViewSet):
    model = LessonAbsence
    
    def get_queryset(self):
        return LessonAbsence.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        return SERIALIZER_ACTION_MAP[self.action]
