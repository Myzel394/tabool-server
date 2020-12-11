from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Teacher

__all__ = [
    "TeacherListSerializer", "TeacherDetailSerializer"
]


class TeacherListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "teacher"
    
    class Meta:
        model = Teacher
        fields = ["short_name", "last_name", "id"]


class TeacherDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "teacher"
    
    class Meta:
        model = Teacher
        fields = [
            "first_name", "last_name", "short_name", "email", "gender", "id"
        ]
