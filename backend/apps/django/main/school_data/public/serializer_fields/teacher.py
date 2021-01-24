from apps.django.utils.serializers import WritableAllFieldMixin
from ...models import Teacher
from ...sub.subserializers.teacher.detail import DetailTeacherSerializer

__all__ = [
    "TeacherField"
]


class TeacherField(WritableAllFieldMixin):
    model = Teacher
    detail_serializer = DetailTeacherSerializer
