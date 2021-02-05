from rest_framework import viewsets

from apps.django.utils.permissions import AuthenticationAndActivePermission, IsTeacherElseReadOnly
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....models import Classbook
from ....serializers import CreateClassbookSerializer, DetailClassbookSerializer, UpdateClassbookSerializer

__all__ = [
    "ClassbookViewSet"
]


class ClassbookViewSet(
    DetailSerializerViewSetMixin,
    viewsets.ModelViewSet,
):
    permission_classes = [AuthenticationAndActivePermission & IsTeacherElseReadOnly]
    detail_serializer = DetailClassbookSerializer
    serializer_action_map = {
        "create": CreateClassbookSerializer,
        "update": UpdateClassbookSerializer,
        "partial_update": UpdateClassbookSerializer,
        "retrieve": DetailClassbookSerializer,
        "list": DetailClassbookSerializer
    }
    
    def get_queryset(self):
        return Classbook.objects.from_user(self.request.user)
