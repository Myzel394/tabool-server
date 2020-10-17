from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin

from apps.django.utils.fields import ColorField
from apps.django.utils.models import UserModelRelationMixin
from ...public import *
from ...public import model_verboses

if TYPE_CHECKING:
    from apps.django.main.school_data.models import Subject

__all__ = [
    "UserSubjectRelation"
]


class UserSubjectRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = model_verboses.SUBJECT_RELATION
        verbose_name_plural = model_verboses.SUBJECT_RELATION_PLURAL
        unique_together = (
            ("subject", "user")
        )
        ordering = ("subject", "user")
    
    subject = models.ForeignKey(
        SUBJECT,
        on_delete=models.CASCADE,
        verbose_name=model_verboses.SUBJECT
    )  # type: Subject
    
    color = ColorField(
        verbose_name=_("Farbe"),
        blank=True,
        null=True,
    )  # type: str
    
    def __str__(self):
        return str(self.subject)
