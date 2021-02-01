from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, hook, LifecycleModel

from apps.django.extra.scooso_scraper.utils import rename_name_for_color_mapping
from apps.django.utils.fields import ColorField
from apps.django.utils.models import UserModelRelationMixin
from ...public import *
from ...public import model_names

if TYPE_CHECKING:
    from apps.django.main.school_data.models import Subject

__all__ = [
    "UserSubjectRelation"
]


class UserSubjectRelation(RandomIDMixin, UserModelRelationMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.SUBJECT_RELATION
        verbose_name_plural = model_names.SUBJECT_RELATION_PLURAL
        unique_together = (
            ("subject", "user")
        )
        ordering = ("subject", "user")
    
    subject = models.ForeignKey(
        SUBJECT,
        on_delete=models.CASCADE,
        verbose_name=model_names.SUBJECT
    )  # type: Subject
    
    color = ColorField(
        verbose_name=_("Farbe"),
        blank=True,
        null=True,
    )  # type: str
    
    def __str__(self):
        return str(self.subject)
    
    @property
    def default_color_for_name(self) -> str:
        return constants.SUBJECT_COLORS_MAPPING.get(rename_name_for_color_mapping(self.subject.name), "#888")
    
    @hook(BEFORE_CREATE)
    def _hook_set_color(self):
        self.color = self.color or self.default_color_for_name
