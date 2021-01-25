from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....filters import AbsenceFilterSet
from ....models import LessonAbsence
from ....paginations import AbsencePagination
from ....serializers import CreateLessonAbsenceSerializer, DetailLessonAbsenceSerializer, UpdateLessonAbsenceSerializer

__all__ = [
    "LessonAbsenceView"
]


class LessonAbsenceView(viewsets.ModelViewSet, DetailSerializerViewSetMixin):
    model = LessonAbsence
    pagination_class = AbsencePagination
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AbsenceFilterSet
    search_fields = ["reason"]
    
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
