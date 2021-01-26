from rest_framework import viewsets

from apps.django.main.authentication.models import User
from apps.django.main.authentication.sub.subserializers.user import UserInformationSerializer, UserUpdateSerializer
from apps.django.utils.viewsets import DetailSerializerViewSetMixin

__all__ = [
    "UserViewSet"
]


class UserViewSet(
    DetailSerializerViewSetMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    detail_serializer = UserInformationSerializer
    serializer_action_map = {
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer,
        "retrieve": UserInformationSerializer
    }
    
    def get_queryset(self):
        return User.objects.only("id").filter(id=self.request.user.id)
