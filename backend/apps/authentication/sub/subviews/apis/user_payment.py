from django.contrib.auth import get_user_model
from rest_framework import viewsets

from ....models import UserPayment
from ....permissions import IsOwnerPermission
from ....serializers import UserPaymentDetailSerializer

__all__ = [
    "UserPaymentViewSet"
]

User = get_user_model()


class UserPaymentViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsOwnerPermission]
    
    def get_serializer_class(self):
        return UserPaymentDetailSerializer
    
    def get_queryset(self):
        return UserPayment.objects.all()
