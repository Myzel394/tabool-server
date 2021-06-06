from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.main.event.models import Exam
from apps.django.main.event.serializers import (
    CreateExamSerializer, StudentDetailExamSerializer,
    StudentListExamSerializer, TeacherDetailExamSerializer, TeacherListExamSerializer, UpdateExamSerializer,
)
from apps.django.main.event.sub.subfilters.exam import ExamFilterSet
from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin

__all__ = [
    "ExamViewSet"
]


class ExamViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExamFilterSet
    search_fields = ["information", "title"]
    ordering_fields = ["date", "title"]

    detail_serializer = {
        STUDENT: StudentDetailExamSerializer,
        TEACHER: TeacherDetailExamSerializer
    }
    serializer_action_map = {
        STUDENT: {
            "detail": StudentDetailExamSerializer,
            "list": StudentListExamSerializer,
        },
        TEACHER: {
            "create": CreateExamSerializer,
            "update": UpdateExamSerializer,
            "partial_update": UpdateExamSerializer,
            "detail": TeacherDetailExamSerializer,
            "list": TeacherListExamSerializer,
        }
    }

    def get_queryset(self):
        return Exam.objects.from_user(self.request.user)
