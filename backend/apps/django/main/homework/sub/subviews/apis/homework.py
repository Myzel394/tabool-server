from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from apps.django.utils.permissions import AuthenticationAndActivePermission, IsStudent, IsTeacher
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....filters import HomeworkFilterSet
from ....models import Homework
from ....serializers import (
    StudentCreateHomeworkSerializer, StudentDetailHomeworkSerializer, StudentListHomeworkSerializer,
    StudentUpdateHomeworkSerializer, TeacherCreateHomeworkSerializer, TeacherDetailHomeworkSerializer,
    TeacherListHomeworkSerializer, TeacherUpdateHomeworkSerializer,
)

__all__ = [
    "StudentHomeworkViewSet", "TeacherHomeworkViewSet"
]


class StudentHomeworkViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsStudent]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HomeworkFilterSet
    search_fields = ["information"]
    ordering_fields = ["due_date"]

    detail_serializer = StudentDetailHomeworkSerializer
    serializer_action_map = {
        "create": StudentCreateHomeworkSerializer,
        "update": StudentUpdateHomeworkSerializer,
        "partial_update": StudentUpdateHomeworkSerializer,
        "list": StudentListHomeworkSerializer,
        "retrieve": StudentDetailHomeworkSerializer
    }

    def check_object_permissions(self, request: RequestType, obj: Homework) -> None:
        if request.method in SAFE_METHODS:
            return

        if obj.private_to_student != request.user.student:
            raise PermissionDenied(_("Du kannst öffentliche Hausaufgaben nicht verändern."))

    def get_queryset(self):
        return Homework.objects.from_user(self.request.user)

    @action(methods=["GET"], detail=False, url_path="homework-information")
    def information(self, request: RequestType):
        homeworks = Homework.objects.from_user(request.user)

        earliest_due_date = homeworks.earliest("due_date").due_date
        latest_due_date = homeworks.latest("due_date").due_date
        private_count = homeworks.only("private_to_student").filter(private_to_student=request.user.student).count()
        completed_count = homeworks \
            .filter(userhomeworkrelation__completed=True) \
            .count()
        ignore_count = homeworks \
            .filter(userhomeworkrelation__ignored=True) \
            .count()
        type_set = set(homeworks.values_list("type", flat=True))
        type_set.discard(None)

        return Response({
            "due_date_min": earliest_due_date,
            "due_date_max": latest_due_date,
            "private_count": private_count,
            "types": list(type_set),
            "completed_count": completed_count,
            "ignore_count": ignore_count
        })


class TeacherHomeworkViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacher]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HomeworkFilterSet
    search_fields = ["information"]
    ordering_fields = ["due_date"]

    detail_serializer = TeacherDetailHomeworkSerializer
    serializer_action_map = {
        "create": TeacherCreateHomeworkSerializer,
        "update": TeacherUpdateHomeworkSerializer,
        "partial_update": TeacherUpdateHomeworkSerializer,
        "list": TeacherListHomeworkSerializer,
        "retrieve": TeacherDetailHomeworkSerializer
    }

    def get_queryset(self):
        return Homework.objects.from_user(self.request.user)
