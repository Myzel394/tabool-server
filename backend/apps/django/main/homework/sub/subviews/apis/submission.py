from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.authentication.user.constants import STUDENT, TEACHER
from apps.django.utils.permissions import (
    AuthenticationAndActivePermission, IsStudentElseReadOnly,
)
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ...subfilters.submission import SubmissionFilterSet
from ....models import Submission
from ....serializers import (
    CreateSubmissionSerializer, StudentDetailSubmissionSerializer, TeacherDetailSubmissionSerializer,
    UpdateSubmissionSerializer,
)

__all__ = [
    "SubmissionViewSet"
]


class SubmissionViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsStudentElseReadOnly]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SubmissionFilterSet
    ordering_fields = ["publish_datetime", "announce"]
    search_fields = ["name"]
    
    detail_serializer = {
        STUDENT: StudentDetailSubmissionSerializer,
        TEACHER: TeacherDetailSubmissionSerializer
    }
    serializer_action_map = {
        STUDENT: {
            "create": CreateSubmissionSerializer,
            "update": UpdateSubmissionSerializer,
            "partial_update": UpdateSubmissionSerializer,
            "retrieve": StudentDetailSubmissionSerializer,
            "list": StudentDetailSubmissionSerializer
        },
        TEACHER: {
            "create": CreateSubmissionSerializer,
            "update": UpdateSubmissionSerializer,
            "partial_update": UpdateSubmissionSerializer,
            "retrieve": TeacherDetailSubmissionSerializer,
            "list": TeacherDetailSubmissionSerializer
        }
    }
    
    def get_queryset(self):
        return Submission.objects.from_user(self.request.user)
