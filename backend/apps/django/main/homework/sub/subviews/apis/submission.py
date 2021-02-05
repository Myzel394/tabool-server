from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import viewsets

from apps.django.utils.permissions import (
    AuthenticationAndActivePermission, IsStudentElseReadOnly,
)
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ...subfilters.submission import SubmissionFilterSet
from ....models import Submission
from ....serializers import CreateSubmissionSerializer, DetailSubmissionSerializer, UpdateSubmissionSerializer

__all__ = [
    "SubmissionViewSet"
]


class SubmissionViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsStudentElseReadOnly]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SubmissionFilterSet
    ordering_fields = ["publish_datetime"]
    
    detail_serializer = DetailSubmissionSerializer
    serializer_action_map = {
        "create": CreateSubmissionSerializer,
        "update": UpdateSubmissionSerializer,
        "partial_update": UpdateSubmissionSerializer,
        "retrieve": DetailSubmissionSerializer,
        "list": DetailSubmissionSerializer
    }
    
    def get_queryset(self):
        return Submission.objects.from_user(self.request.user)
