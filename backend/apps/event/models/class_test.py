from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models import RandomIDMixin

from apps.subject import model_references, model_verbose_functions


class ClassTest(RandomIDMixin):
    class Meta:
        verbose_name = _("Klassenarbeit")
        verbose_name_plural = _("Klassenarbeiten")
    
    lesson = models.ForeignKey(
        model_references.LESSON,
        on_delete=models.CASCADE,
        verbose_name=model_verbose_functions.lesson_single,
    )
