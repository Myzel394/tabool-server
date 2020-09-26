from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from apps.utils import UserModelRelationMixin
from ...public import model_references, model_verbose_functions

__all__ = [
    "UserHomeworkRelation"
]


class UserHomeworkRelation(RandomIDMixin, UserModelRelationMixin):
    class Meta:
        verbose_name = _("Benutzer-Hausaufgabe-Beziehung")
        verbose_name_plural = _("Benutzer-Hausaufgaben-Beziehungen")
    
    homework = models.ForeignKey(
        model_references.HOMEWORK,
        verbose_name=model_verbose_functions.homework_single,
        on_delete=models.CASCADE,
    )
    
    completed = models.BooleanField(
        default=False,
        verbose_name=_("Erledigt")
    )
