from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from ....filters import SubmissionFilterSet
from ....models import Submission
from ....serializers import SubmissionDetailSerializer, SubmissionListSerializer

__all__ = [
    "SubmissionViewSet"
]


class SubmissionViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SubmissionFilterSet
    ordering_fields = ["upload_at", "is_uploaded"]
    
    def get_queryset(self):
        return Submission.objects.user_accessible(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return SubmissionListSerializer
        return SubmissionDetailSerializer
