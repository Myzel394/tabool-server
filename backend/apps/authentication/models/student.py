from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from apps.school_data.public import *
from .. import constants
from ..exceptions import CannotChangeUserError, UserNotActivatedError
from ..public import *

if TYPE_CHECKING:
    from . import User

__all__ = [
    "Student"
]


class Student(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Schüler")
        verbose_name_plural = _("Schüler")
        ordering = ("user", "class_number")
    
    user = models.OneToOneField(
        USER,
        verbose_name=user_single,
        on_delete=models.CASCADE,
    )  # type: User
    
    class_number = models.PositiveSmallIntegerField(
        choices=[
            (number, number)
            for number in constants.AVAILABLE_CLASS_NUMBERS
        ],
        verbose_name=_("Klassenstufe")
    )
    
    main_teacher = models.ForeignKey(
        TEACHER,
        verbose_name=teacher_single,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    
    @hook(BEFORE_UPDATE, when="user", has_changed=True)
    def _hook_validate_user_cant_change(self):
        raise CannotChangeUserError(_("Der Benutzer kann nicht verändert werden."))
    
    @hook(BEFORE_CREATE)
    def _hook_validate_user_activated(self):
        if not self.user.is_active:
            raise UserNotActivatedError(_("Der Benutzer ist noch nicht aktiviert worden!"))
