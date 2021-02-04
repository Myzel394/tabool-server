from .base import BaseUserSerializer
from ..preference import DetailPreferenceSerializer

__all__ = [
    "DetailUserSerializer", "UserInformationSerializer"
]


class DetailUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "first_name", "last_name", "email", "id"
        ]


class UserInformationSerializer(BaseUserSerializer):
    fields = [
        "has_filled_out_data", "preference", "is_confirmed", "first_name", "last_name",
        "email", "id"
    ]
    
    preference = DetailPreferenceSerializer()
