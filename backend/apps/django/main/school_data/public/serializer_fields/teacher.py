from apps.django.main.school_data.models import Teacher
from apps.django.main.school_data.sub.subserializers.teacher import TeacherDetailSerializer
from apps.django.utils.serializers import WritableAllFieldMixin

__all__ = [
    "TeacherField"
]


class TeacherField(WritableAllFieldMixin):
    model = Teacher
    detail_serializer = TeacherDetailSerializer
