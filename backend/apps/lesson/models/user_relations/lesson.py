from django.utils.translation import gettext_lazy as _
from django.db import models
from django_common_utils.libraries.models import RandomIDMixin

from ...public import model_references, model_verbose_functions


class UserLessonRelation(RandomIDMixin):
    class Meta:
        verbose_name = _("Benutzer-Stunde-Beziehung")
        verbose_name_plural = _("Benutzer-Stunden-Beziehungen")
    
    lesson = models.ForeignKey(
        model_references.LESSON,
        verbose_name=model_verbose_functions.lesson_single,
        on_delete=models.CASCADE,
    )
    
    attendance = models.BooleanField(
        default=True,
        verbose_name=_("Anwesend?"),
        help_text=_("Bist du in dieser Stunde anwesend?")
    )

# TODO: Das hier später hinzufügen!
