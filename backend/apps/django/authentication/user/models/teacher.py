from typing import *

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

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
    
    def clean(self):
        if not self.user.is_confirmed:
            raise ValidationError(_("Bestätige deine E-Mail."))
        
        if self.has_changed("user.id"):
            raise ValidationError(_("Der Benutzer kann nicht verändert werden."))
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="user.id", has_changed=True)
    def _hook_call_full_clean(self):
        self.full_clean()
