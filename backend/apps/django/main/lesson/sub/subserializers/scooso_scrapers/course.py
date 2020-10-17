from apps.django.utils.serializers import GetOrCreateSerializerMixin
from ....models import Course

__all__ = [
    "CourseScoosoScraperSerializer"
]


class CourseScoosoScraperSerializer(GetOrCreateSerializerMixin):
    class Meta:
        model = Course
        fields = [
            "course_number",
        ]
