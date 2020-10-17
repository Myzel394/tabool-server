from typing import *

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.django.main.school_data.public import *
from apps.django.main.school_data.public import model_verboses as school_verboses
from .. import constants
from ..public import *
from ..public import model_verboses

if TYPE_CHECKING:
    from . import User
    from apps.django.main.school_data.models import Teacher

__all__ = [
    "Student"
]


class Student(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_verboses.STUDENT
        verbose_name_plural = model_verboses.STUDENT_PLURAL
        ordering = ("user", "class_number")
    
    user = models.OneToOneField(
        USER,
        on_delete=models.CASCADE,
        verbose_name=model_verboses.USER,
    )  # type: User
    
    main_teacher = models.ForeignKey(
        TEACHER,
        on_delete=models.SET_NULL,
        verbose_name=school_verboses.TEACHER,
        blank=True,
        null=True,
    )  # type: Teacher
    
    class_number = models.PositiveSmallIntegerField(
        choices=[
            (number, number)
            for number in constants.AVAILABLE_CLASS_NUMBERS
        ],
        verbose_name=_("Klassenstufe")
    )  # type: int
    
    def __str__(self):
        return _("{user} in Klasse {class_number} mit Lehrer {teacher}").format(
            user=self.user,
            class_number=self.class_number,
            teacher=self.main_teacher
        )
    
    def clean(self):
        if not self.user.is_confirmed:
            raise ValidationError(_("Der Benutzer ist noch nicht aktiviert!"))
        
        if self.has_changed("user"):
            raise ValidationError(_("Der Benutzer kann nicht verändert werden."))
        
        return super().clean()
    
    @hook(BEFORE_UPDATE, when="user", has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @hook(BEFORE_CREATE)
    def _hook_validate_user_activated(self):
        self.full_clean()
