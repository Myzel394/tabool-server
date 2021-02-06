from rest_framework import viewsets

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.main.event.models import Exam
from apps.django.main.event.serializers import (
    CreateExamSerializer, StudentDetailExamSerializer,
    StudentListExamSerializer, TeacherDetailExamSerializer, TeacherListExamSerializer, UpdateExamSerializer,
)
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
    detail_serializer = {
        STUDENT: StudentDetailExamSerializer,
        TEACHER: TeacherDetailExamSerializer
    }
    serializer_action_map = {
        STUDENT: {
            "create": CreateExamSerializer,
            "update": UpdateExamSerializer,
            "partial_update": UpdateExamSerializer,
            "detail": StudentDetailExamSerializer,
            "list": StudentListExamSerializer,
        },
        TEACHER: {
            "detail": TeacherDetailExamSerializer,
            "list": TeacherListExamSerializer,
        }
    }
    
    def get_queryset(self):
        return Exam.ordering.from_user(self.request.user)
