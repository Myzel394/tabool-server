from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

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
            "retrieve": TeacherDetailSubmissionSerializer,
            "list": TeacherDetailSubmissionSerializer
        }
    }
    
    def get_queryset(self):
        return Submission.objects.from_user(self.request.user)
    
    @action(["POST"], detail=True)
    def upload(self, request: RequestType, pk):
        submission = self.get_object()
        serializer_context = {
            "request": request
        }
        serializer = self.get_detail_serializer()
        
        if submission.publish_datetime and submission.publish_datetime < datetime.now():
            serializer_instance = serializer(instance=submission, context=serializer_context)
            return Response(serializer_instance.data, status=status.HTTP_202_ACCEPTED)
        
        submission.publish_datetime = datetime.now()
        submission.save()
        
        serializer_instance = serializer(instance=submission, context=serializer_context)
        
        return Response(serializer_instance.data)
