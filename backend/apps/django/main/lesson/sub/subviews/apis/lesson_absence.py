from rest_framework import viewsets

from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....models import LessonAbsence
from ....serializers import CreateLessonAbsenceSerializer, DetailLessonAbsenceSerializer, UpdateLessonAbsenceSerializer

__all__ = [
    "LessonAbsenceView"
]


class LessonAbsenceView(viewsets.ModelViewSet, DetailSerializerViewSetMixin):
    model = LessonAbsence
    detail_serializer = DetailLessonAbsenceSerializer
    serializer_action_map = {
        "list": DetailLessonAbsenceSerializer,
        "retrieve": DetailLessonAbsenceSerializer,
        "create": CreateLessonAbsenceSerializer,
        "update": UpdateLessonAbsenceSerializer,
        "partial_update": UpdateLessonAbsenceSerializer,
    }
    
    def get_queryset(self):
        return LessonAbsence.objects.from_user(self.request.user)
