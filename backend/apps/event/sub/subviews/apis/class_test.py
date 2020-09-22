from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.event.models import ClassTest
from ....serializers import ClassTestDetailSerializer, ClassTestListSerializer

__all__ = [
    "ClassTestViewSet"
]


class ClassTestViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return ClassTest.objects.from_queryset(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return ClassTestListSerializer
        return ClassTestDetailSerializer
