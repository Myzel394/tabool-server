from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from .material import MaterialDetailSerializer as BaseMaterialSerializer
from ...models import Material

__all__ = [
    "MaterialListSerializer", "MaterialDetailEndpointSerializer", "UploadSerializer",
]


class MaterialListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "material"
    
    class Meta:
        model = Material
        fields = [
            "lesson", "name", "added_at", "id"
        ]


class MaterialDetailEndpointSerializer(BaseMaterialSerializer):
    class Meta:
        model = Material
        fields = [
            "name", "added_at", "lesson", "id", "file", "scooso_download_link"
        ]
    
    file = serializers.SerializerMethodField()
    scooso_download_link = serializers.SerializerMethodField()
    
    def get_file(self, instance: Material) -> Optional[str]:
        return instance.file.url
    
    def get_scooso_download_link(self, instance: Material) -> str:
        return instance.get_scooso_download_link(self.context["request"].user)


class UploadSerializer(serializers.Serializer):
    lesson = LessonField()
    file = serializers.FileField(label=_("Datei"))
