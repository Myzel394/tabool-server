from typing import *

from django.core.files.uploadedfile import InMemoryUploadedFile
from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from apps.django.extra.scooso_scraper.scrapers.material import *
from apps.django.utils.viewsets import BulkDeleteMixin
from ...subserializers.material__endpoint import UploadSerializer
from ...subserializers.submission__endpoint import SubmissionEndpointDetailSerializer
from .... import constants
from ....filters import SubmissionFilterSet
from ....models import Submission
from ....serializers import SubmissionListSerializer

__all__ = [
    "SubmissionViewSet"
]


class SubmissionViewSet(viewsets.ModelViewSet, BulkDeleteMixin):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SubmissionFilterSet
    ordering_fields = ["upload_date", "is_uploaded"]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        return Submission.objects.user_accessible(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return SubmissionListSerializer
        return SubmissionEndpointDetailSerializer
    
    @action(detail=False, methods=["post"])
    def scooso(self, request: RequestType):
        """Uploads a given file directly to Scooso."""
        
        # Preparation
        user = request.user
        data = request.data
        serializer = UploadSerializer(data=data, context={
            "request": request
        })
        
        # Validation
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get data
        validated_data = serializer.validated_data
        lesson = validated_data["lesson"]
        file: InMemoryUploadedFile = validated_data["file"]
        
        # Get scraper data
        time_id = lesson.lessonscoosodata.time_id
        targeted_date = lesson.date
        filename = file.name
        data = file.read()
        material_type = MaterialTypeOptions.HOMEWORK
        
        scraper = MaterialRequest(user.scoosodata.username, user.scoosodata.password)
        scraper.login()
        
        # Upload
        try:
            scraper.upload_material(
                time_id=time_id,
                targeted_date=targeted_date,
                filename=filename,
                data=data,
                material_type=material_type
            )
        except:
            return Response({
                "upload_status": constants.UPLOAD_STATUSES.FAILED
            }, status=status.HTTP_502_BAD_GATEWAY)
        return Response({
            "upload_status": constants.UPLOAD_STATUSES.UPLOADED
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post", "get"])
    def upload(self, request: RequestType, pk: Optional[str] = None):
        submission = self.get_object()
        
        if submission.is_uploaded:
            return Response({
                "upload_status": constants.UPLOAD_STATUSES.UPLOADED
            }, status=status.HTTP_202_ACCEPTED)
        
        if submission.is_in_action:
            return Response({
                "upload_status": constants.UPLOAD_STATUSES.PENDING
            }, status=status.HTTP_202_ACCEPTED)
        
        if request.method == "POST":
            try:
                submission.upload_file()
            except:
                return Response({
                    "upload_status": constants.UPLOAD_STATUSES.FAILED
                }, status=status.HTTP_502_BAD_GATEWAY)
            return Response({
                "upload_status": constants.UPLOAD_STATUSES.UPLOADED
            }, status=status.HTTP_200_OK)
        elif request.method == "GET":
            return Response({
                "upload_status": constants.UPLOAD_STATUSES.RESTING
            }, status=status.HTTP_200_OK)
