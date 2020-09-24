from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin, TextOptimizerHandler
from django_common_utils.libraries.models import RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel

from ...subject.public import model_references, model_verbose_functions
from ..querysets import ClassTestQuerySet

__all__ = [
    "ClassTest"
]

from apps.utils.validators import validate_weekday_in_lesson_data_available


class ClassTest(RandomIDMixin, LifecycleModel, HandlerMixin):
    class Meta:
        verbose_name = _("Klassenarbeit")
        verbose_name_plural = _("Klassenarbeiten")
    
    objects = ClassTestQuerySet.as_manager()
    
    subject = models.ForeignKey(
        model_references.SUBJECT,
        on_delete=models.CASCADE,
        verbose_name=model_verbose_functions.subject_single,
    )
    
    room = models.ForeignKey(
        model_references.ROOM,
        on_delete=models.CASCADE,
        verbose_name=model_verbose_functions.room_single,
        blank=True,
        null=True
    )
    
    targeted_date = models.DateField(
        verbose_name=_("Datum"),
        help_text=_("Datum, wann die Klassenarbeit geschrieben wird.")
    )
    
    information = models.TextField(
        verbose_name=_("Informationen"),
        blank=True,
        null=True
    )
    
    @staticmethod
    def handlers():
        return {
            "information": TextOptimizerHandler()
        }
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when="targeted_date")
    def _hook_validate_targeted_dae(self):
        validate_weekday_in_lesson_data_available(self.targeted_date)
