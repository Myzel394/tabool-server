from rest_framework import serializers

from ....models import Course

__all__ = [
    "CourseScoosoScraperSerializer"
]


class CourseScoosoScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "course_number",
        ]
