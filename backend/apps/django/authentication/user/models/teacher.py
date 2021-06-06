from typing import *

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_DELETE, BEFORE_SAVE, BEFORE_UPDATE, hook

from apps.django.utils.models import IdMixin
from ..public import *
from ..public import model_names

if TYPE_CHECKING:
    from ..models import User

__all__ = [
    "Teacher"
]


class Teacher(IdMixin):
    class Meta:
        verbose_name = model_names.TEACHER
        verbose_name_plural = model_names.TEACHER_PLURAL
        ordering = ("user",)

    user = models.OneToOneField(
        USER,
        on_delete=models.CASCADE,
        verbose_name=model_names.USER,
    )  # type: User

    short_name = models.CharField(
        verbose_name=_("Initialien"),
        max_length=32
    )  # type: str

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.short_name})"

    @hook(BEFORE_UPDATE, when="user.id", has_changed=True, was_not=None)
    def _hook_cant_change_user(self):  # skipcq: PYL-R0201
        raise ValidationError(_("Der Benutzer kann nicht verändert werden."))

    @hook(BEFORE_SAVE, when="user.is_confirmed", is_now=False)
    def _hook_email_must_be_confirmed(self):  # skipcq: PYL-R0201
        raise ValidationError(_("Bestätige deine E-Mail."))

    @hook(AFTER_DELETE)
    def _hook_delete_user(self):
        self.user.delete()
