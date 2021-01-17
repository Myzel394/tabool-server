from typing import *

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_hint import *
from django_lifecycle import BEFORE_SAVE, hook, LifecycleModel

from apps.django.main.authentication.public import model_names as auth_names
from ..public.model_names import POLL_NAME, POLL_NAME_PLURAL
from ..querysets import PollQuerySet

if TYPE_CHECKING:
    from .choice import Choice

__all__ = [
    "Poll"
]


class Poll(RandomIDMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = POLL_NAME
        verbose_name_plural = POLL_NAME_PLURAL
        ordering = ("title", "created_at")
    
    objects = PollQuerySet.as_manager()
    
    title = models.TextField(
        max_length=63,
        verbose_name=_("Titel")
    )
    
    max_vote_date = models.DateTimeField(
        verbose_name=_("Maximal Datum zum Abstimmen"),
        blank=True,
        null=True,
    )
    
    show_results_date = models.DateTimeField(
        verbose_name=_("Veröffentlichkeitsdatum der Ergebnisse"),
        help_text=_("Ab wann man die Ergebnisse schauen kann"),
        blank=True,
        null=True,
    )
    
    max_vote_choices = models.PositiveSmallIntegerField(
        verbose_name=_("Maximale Abstimmmöglichkeiten"),
        help_text=_("Wie viele Elemente maximal ausgewählt werden können"),
        default=1
    )
    
    targeted_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=auth_names.USER_PLURAL,
    )
    
    @hook(BEFORE_SAVE)
    def _hook_validate_max_vote_choices(self):
        length = self.choices.count()
        
        if 0 < length <= self.max_vote_choices:
            raise ValidationError(_(
                f"Ungültige Eingabe für das Feld \"{self._meta.get_field('max_vote_choices').verbose_name}\", "
                f"der Wert muss kleiner sein als die Anzahl der Auswahlmöglichkeiten."))
    
    @property
    def choices(self) -> QueryType["Choice"]:
        return self.choice_set.all()
