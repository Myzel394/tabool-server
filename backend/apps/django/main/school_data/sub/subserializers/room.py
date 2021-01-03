from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from apps.django.utils.validators import validate_place
from ...models import Room

__all__ = [
    "RoomDetailSerializer"
]


class RoomDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "room"
    
    class Meta:
        model = Room
        fields = ["place", "id"]
        read_only_fields = ["place"]
    
    place = serializers.CharField(
        validators=[validate_place, UniqueValidator(queryset=Room.objects.all())],
    )
