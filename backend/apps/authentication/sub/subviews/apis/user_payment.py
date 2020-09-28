from django.contrib.auth import get_user_model
from rest_framework import viewsets

from ....permissions import UserPaymentAccessPermission
from ....serializers import UserPaymentDetailSerializer, ManageUserPaymentSerializer
from ....models import UserPayment

__all__ = [
    "UserPaymentViewSet"
]

User = get_user_model()


class UserPaymentViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [UserPaymentAccessPermission]
    
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return ManageUserPaymentSerializer
        return UserPaymentDetailSerializer
    
    def get_queryset(self):
        return UserPayment.objects.all()

# TODO: Global permission classes!

