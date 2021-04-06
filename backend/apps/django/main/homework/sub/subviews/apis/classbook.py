from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....filters import ClassbookFilterSet
from ....models import Classbook
from ....serializers import (
    CreateClassbookSerializer, StudentDetailClassbookSerializer,
    TeacherDetailClassbookSerializer, UpdateClassbookSerializer,
)

__all__ = [
    "ClassbookViewSet"
]


class ClassbookViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]
    detail_serializer = {
        STUDENT: StudentDetailClassbookSerializer,
        TEACHER: TeacherDetailClassbookSerializer,
    }
    serializer_action_map = {
        STUDENT: {
            "retrieve": StudentDetailClassbookSerializer,
            "list": StudentDetailClassbookSerializer
        },
        TEACHER: {
            "create": CreateClassbookSerializer,
            "update": UpdateClassbookSerializer,
            "partial_update": UpdateClassbookSerializer,
            "retrieve": TeacherDetailClassbookSerializer,
            "list": TeacherDetailClassbookSerializer
        }
    }

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClassbookFilterSet
    search_fields = ["online_content", "presence_content"]
    ordering_fields = ["lesson_date"]

    def get_queryset(self):
        return Classbook.objects.from_user(self.request.user)
