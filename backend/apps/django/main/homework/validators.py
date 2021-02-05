from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime

if TYPE_CHECKING:
    from .models import Homework

__all__ = [
    "validate_private_to_user", "only_future"
]


def validate_private_to_user(homework: "Homework") -> None:
    user = homework.private_to_user
    
    if user:
        available_users = homework.lesson.course.participants.all()
        
        if user not in available_users:
            raise ValidationError({
                "private_to_user": _("Dieser Benutzer ist kein Mitglied des Kurses {course}.").format(
                    course=homework.lesson.course.name
                )})


def only_future(value: "datetime") -> None:
    if value and value < datetime.now():
        raise ValidationError(
            _("Das Veröffentlichkeitsdatum muss in der Zukunft liegen")
        )
