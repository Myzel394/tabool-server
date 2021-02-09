from rest_framework import viewsets

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
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
    
    def get_queryset(self):
        return Classbook.objects.from_user(self.request.user)
