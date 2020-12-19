from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import (
    PreferredIdsMixin, RandomIDSerializerMixin,
)
from .submission import FilenameMixin, SizeMixin, SubmissionDetailSerializer
from ...models import Submission

__all__ = [
    "SubmissionListSerializer", "SubmissionEndpointDetailSerializer"
]


class SubmissionListSerializer(
    RandomIDSerializerMixin,
    FilenameMixin,
    SizeMixin,
    PreferredIdsMixin,
):
    preferred_id_key = "submission"
    
    class Meta:
        model = Submission
        fields = [
            "lesson", "filename", "size", "id"
        ]
    
    lesson = LessonField()


class SubmissionEndpointDetailSerializer(SubmissionDetailSerializer, SizeMixin):
    class Meta(SubmissionDetailSerializer.Meta):
        fields = SubmissionDetailSerializer.Meta.fields + [
            "lesson",
        ]
    
    lesson = LessonField(detail=True)
