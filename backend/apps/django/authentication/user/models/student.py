from typing import *

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_DELETE, BEFORE_SAVE, BEFORE_UPDATE, hook

from apps.django.utils.models import IdMixin
from .. import constants
from ..public import *
from ..public import model_names

if TYPE_CHECKING:
    from . import User, Teacher

__all__ = [
    "Student"
]


class Student(IdMixin):
    class Meta:
        verbose_name = model_names.STUDENT
        verbose_name_plural = model_names.STUDENT_PLURAL
        ordering = ("user", "class_number")
    
    user = models.OneToOneField(
        USER,
        on_delete=models.CASCADE,
        verbose_name=model_names.USER,
    )  # type: User
    
    main_teacher = models.ForeignKey(
        TEACHER,
        on_delete=models.SET_NULL,
        verbose_name=model_names.TEACHER,
        null=True
    )  # type: Teacher
    
    class_number = models.PositiveSmallIntegerField(
        choices=[
            (number, number)
            for number in constants.AVAILABLE_CLASS_NUMBERS
        ],
        verbose_name=_("Klassenstufe")
    )  # type: int
    
    def __str__(self):
        return _("{user} in Klasse {class_number} mit Kurslehrer {teacher}").format(
            user=self.user,
            class_number=self.class_number,
            teacher=self.main_teacher
        )
    
    @hook(BEFORE_UPDATE, when="user.id", has_changed=True, was_not=None)
    def _hook_cant_change_user(self):
        raise ValidationError(_("Der Benutzer kann nicht verändert werden."))
    
    @hook(BEFORE_SAVE, when="user.is_confirmed", is_now=False)
    def _hook_email_must_be_confirmed(self):
        raise ValidationError(_("Bestätige deine E-Mail."))
    
    @hook(AFTER_DELETE)
    def _hook_delete_user(self):
        self.user.delete()
    
    @property
    def class_level(self) -> constants.ClassLevel:
        return constants.ClassLevel.PRIMARY if self.class_number <= 10 else constants.ClassLevel.SECONDARY
