from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import (
    PreferredIdsMixin, RandomIDSerializerMixin,
)
from .submission import FilenameMixin, SubmissionDetailSerializer
from ...models import Submission

__all__ = [
    "SubmissionListSerializer", "SubmissionEndpointDetailSerializer"
]


class SubmissionListSerializer(RandomIDSerializerMixin, FilenameMixin, PreferredIdsMixin):
    preferred_id_key = "submission"
    
    class Meta:
        model = Submission
        fields = [
            "lesson", "filename", "upload_at", "id"
        ]
    
    lesson = LessonField()


class SubmissionEndpointDetailSerializer(SubmissionDetailSerializer):
    class Meta(SubmissionDetailSerializer.Meta):
        fields = SubmissionDetailSerializer.Meta.fields + [
            "lesson",
        ]
    
    lesson = LessonField(detail=True)
