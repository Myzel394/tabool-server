from rest_framework import serializers

from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Material

__all__ = [
    "MaterialDetailSerializer"
]


class MaterialDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Material
        fields = [
            "file", "name", "added_at", "scooso_download_link", "id"
        ]
    
    scooso_download_link = serializers.SerializerMethodField()
    
    def get_scooso_download_link(self):
        user = self.context["request"]
        url = self.instance.materialscoosodata.build_download_url(user)
        
        return url
