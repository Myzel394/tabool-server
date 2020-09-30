from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.utils import UserModelRelationMixin
from apps.utils.fields import ColorField
from ...public import *

if TYPE_CHECKING:
    from .. import Subject

__all__ = [
    "UserSubjectRelation"
]


class UserSubjectRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = _("Benutzer-Fach-Beziehung")
        verbose_name_plural = _("Benutzer-Fächer-Beziehungen")
        unique_together = (
            ("subject", "user")
        )
        ordering = ("subject", "user")
    
    subject = models.ForeignKey(
        SUBJECT,
        verbose_name=subject_single,
        on_delete=models.CASCADE
    )  # type: Subject
    
    color = ColorField(
        verbose_name=_("Farbe"),
        blank=True,
        null=True,
    )
