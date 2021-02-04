from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.utils.viewsets import DetailSerializerViewSetMixin, RetrieveFromUserMixin
from ....models import Course
from ....serializers import (
    StudentDetailCourseSerializer, StudentListCourseSerializer, TeacherDetailCourseSerializer,
    TeacherListCourseSerializer,
)

__all__ = [
    "CourseViewSet"
]


class CourseViewSet(
    viewsets.mixins.ListModelMixin,
    RetrieveFromUserMixin,
    DetailSerializerViewSetMixin
):
    filter_backends = [SearchFilter]
    search_fields = ["subject__name", "course_number", "teacher__last_name"]
    model = Course
    detail_serializer = {
        STUDENT: StudentDetailCourseSerializer,
        TEACHER: TeacherDetailCourseSerializer
    }
    serializer_action_map = {
        STUDENT: {
            "list": StudentListCourseSerializer,
        },
        TEACHER: {
            "list": TeacherListCourseSerializer
        }
    }
