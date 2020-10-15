from typing import *

from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .... import constants
from ....filters import SubmissionFilterSet
from ....models import Submission
from ....serializers import SubmissionDetailSerializer, SubmissionListSerializer, UploadSerializer

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
    
    @action(detail=False, methods=["post"], url_path="upload-directly")
    def upload_directly(self, request: RequestType):
        data = request.data
        serializer = UploadSerializer(data=data, context={
            "request": request
        })
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        lesson = validated_data["lesson"]
        
        time_id = lesson.lessonscoosodata.time_id
        targeted_date = lesson.date
        filename = validated_data["file"]
    
    @action(detail=True, methods=["post", "get"])
    def upload(self, request: RequestType, pk: Optional[str] = None):
        submission = self.get_object()
        
        if submission.is_uploaded:
            return Response({
                "upload_status": constants.UPLOAD_STATUSES.UPLOADED
            }, status=status.HTTP_202_ACCEPTED)
        
        if submission.is_uploading:
            return Response({
                "upload_status": constants.UPLOAD_STATUSES.PENDING
            }, status=status.HTTP_202_ACCEPTED)
        
        if request.method == "POST":
            try:
                submission.upload_file()
            except:
                upload_status = constants.UPLOAD_STATUSES.FAILED
            else:
                upload_status = constants.UPLOAD_STATUSES.UPLOADED
        elif request.method == "GET":
            upload_status = constants.UPLOAD_STATUSES.RESTING
        
        return Response({
            "upload_status": upload_status
        }, status=status.HTTP_200_OK)
