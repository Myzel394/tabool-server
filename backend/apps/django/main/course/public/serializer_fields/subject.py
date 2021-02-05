from apps.django.main.course.models import Subject
from apps.django.utils.serializers import WritableAllFieldMixin

__all__ = [
    "SubjectField"
]


class SubjectField(WritableAllFieldMixin):
    model = Subject
