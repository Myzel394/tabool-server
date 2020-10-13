from typing import *

from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.utils.threads import run_in_thread
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
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return Submission.objects.user_accessible(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return SubmissionListSerializer
        return SubmissionDetailSerializer
    
    @action(detail=True, methods=["post", "get"])
    def upload(self, request: RequestType, pk: Optional[str] = None):
        PENDING = "PENDING"
        UPLOADED = "UPLOADED"
        RESTING = "RESTING"
        
        submission = self.get_object()
        
        if submission.is_uploaded:
            return Response({
                "upload_status": UPLOADED
            }, status=status.HTTP_202_ACCEPTED)
        
        if submission.is_uploading:
            return Response({
                "upload_status": PENDING
            }, status=status.HTTP_202_ACCEPTED)
        
        if request.method == "POST":
            run_in_thread(submission.upload_file)
            return Response({
                "upload_status": PENDING
            }, status=status.HTTP_200_OK)
        elif request.method == "GET":
            return Response({
                "upload_status": RESTING
            }, status=status.HTTP_202_ACCEPTED)
