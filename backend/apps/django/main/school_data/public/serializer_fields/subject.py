from apps.django.main.school_data.models import Subject
from apps.django.main.school_data.sub.subserializers.subject import SubjectDetailSerializer
from apps.django.utils.serializers import WritableAllFieldMixin

__all__ = [
    "SubjectField"
]


class SubjectField(WritableAllFieldMixin):
    model = Subject
    detail_serializer = SubjectDetailSerializer
