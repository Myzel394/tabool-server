from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.handlers import HandlerMixin, TextOptimizerHandler
from django_common_utils.libraries.models import RandomIDMixin

from apps.subject import model_references, model_verbose_functions

__all__ = [
    "ClassTest"
]


class ClassTest(RandomIDMixin, HandlerMixin):
    class Meta:
        verbose_name = _("Klassenarbeit")
        verbose_name_plural = _("Klassenarbeiten")
    
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
