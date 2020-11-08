from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields import LessonField
from apps.django.utils.serializers import RandomIDSerializerMixin
from ...models import Material

__all__ = [
    "MaterialListSerializer", "MaterialDetailSerializer", "UploadSerializer",
]


class MaterialListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Material
        fields = [
            "name", "added_at", "id"
        ]


class MaterialDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Material
        fields = [
            "file", "name", "added_at", "scooso_download_link", "id"
        ]
    
    scooso_download_link = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    
    def get_scooso_download_link(self, instance: Material):
        if scooso_data := getattr(instance, "materialscoosodata", None):
            user = self.context["request"].user
            url = scooso_data.build_download_url(user)
            return url
        return
    
    def get_file(self, instance: Material):
        return instance.file.url


class UploadSerializer(serializers.Serializer):
    lesson = LessonField()
    file = serializers.FileField(label=_("Datei"))
