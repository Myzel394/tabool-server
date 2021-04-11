from datetime import datetime
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ...utils.time import get_now

if TYPE_CHECKING:
    from .models import Homework

__all__ = [
    "validate_private_to_student", "only_future"
]


def validate_private_to_student(homework: "Homework") -> None:
    student = homework.private_to_student
    
    if student:
        available_students = homework.lesson.course.participants.all()
        
        if student not in available_students:
            raise ValidationError({
                "private_to_student": _("Dieser Benutzer ist kein Mitglied des Kurses {course}.").format(
                    course=homework.lesson.course.name
                )})


def only_future(value: "datetime") -> None:
    if value and value <= get_now():
        raise ValidationError(
            _("Das Veröffentlichkeitsdatum muss in der Zukunft liegen")
        )
