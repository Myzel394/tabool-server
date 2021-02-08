from typing import *

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.django.authentication.user.public.serializer_fields.student import StudentField
from .base import BaseHomeworkSerializer

if TYPE_CHECKING:
    from ....models import Homework
    from apps.django.authentication.user.models import Student

__all__ = [
    "StudentUpdateHomeworkSerializer", "TeacherUpdateHomeworkSerializer"
]


class StudentUpdateHomeworkSerializer(BaseHomeworkSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type",
        ]


class TeacherUpdateHomeworkSerializer(BaseHomeworkSerializer):
    instance: "Homework"
    
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "due_date", "information", "type", "private_to_student"
        ]
    
    private_to_student = StudentField(required=False)
    
    def validate_private_to_student(self, value: "Student"):
        if self.instance.private_to_student is not None and value is not None:
            raise ValidationError(
                _("Öffentliche Hausaufgaben können nicht mehr privat gestellt werden.")
            )
