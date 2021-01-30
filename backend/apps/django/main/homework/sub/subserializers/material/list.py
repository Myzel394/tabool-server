from typing import *

from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.main.school_data.sub.subserializers.subject import SubjectSerializer
from .base import BaseMaterialSerializer
from ..mixins import SizeMixin

if TYPE_CHECKING:
    from ....models import Material

__all__ = [
    "ListMaterialSerializer"
]


class ListMaterialSerializer(BaseMaterialSerializer, SizeMixin):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "subject", "name", "added_at", "size", "id"
        ]
    
    lesson = LessonField()
    
    subject = serializers.SerializerMethodField()
    
    def get_subject(self, instance: "Material"):
        return SubjectSerializer(instance=instance.lesson.course.subject, context=self.context).data
