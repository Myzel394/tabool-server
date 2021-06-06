from rest_framework import viewsets

from ....models import User
from ....serializers import UserInformationSerializer

__all__ = [
    "UserViewSet"
]


class UserViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.RetrieveModelMixin,
):
    serializer_class = UserInformationSerializer

    def get_queryset(self):
        return User.objects.only("id").filter(id=self.request.user.id)
