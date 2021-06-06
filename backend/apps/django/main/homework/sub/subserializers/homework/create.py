from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.django.authentication.user.public.serializer_fields.student import StudentField
from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseHomeworkSerializer

__all__ = [
    "StudentCreateHomeworkSerializer", "TeacherCreateHomeworkSerializer"
]


class StudentCreateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type", "lesson", "lesson_date",
        ]

    lesson = LessonField()

    def create(self, validated_data):
        validated_data["private_to_student"] = self.context["request"].user.student

        return super().create(validated_data)


class TeacherCreateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type", "lesson", "lesson_date",

            "private_to_student"
        ]

    lesson = LessonField()
    private_to_student = StudentField(required=False, allow_null=True)

    def validate(self, attrs):
        student = attrs.get("private_to_student")
        lesson = attrs["lesson"]

        if student:
            available_students = lesson.course.participants.all()

            if student not in available_students:
                raise ValidationError({
                    "private_to_student": _("Dieser Benutzer ist kein Mitglied des Kurses {course}.").format(
                        course=lesson.course.name
                    )})

        return super().validate(attrs)
