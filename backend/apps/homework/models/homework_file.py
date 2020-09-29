from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import BEFORE_UPDATE, hook

from apps.authentication.public import model_references
from apps.utils.models import AddedAtMixin


# TODO: Add multiple databases!
class HomeworkFile(RandomIDMixin, AddedAtMixin):
    class Meta:
        verbose_name = _("Datei")
        verbose_name_plural = _("Dateien")
    
    owner = models.ForeignKey(
        model_references.USER,
        verbose_name=_("Besitzer"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    
    send_on = models.DateTimeField(
        verbose_name=_("Sendedatum"),
        help_text=_("Wann soll die Datei geschickt werden?"),
        blank=True,
        null=True
    )
    
    is_online = models.BooleanField(
        default=False,
        verbose_name=_("Hochgeladen"),
        help_text=_("Wurde die Datei hochgeladen?")
    )
    
    actual_file = models.FileField(
        verbose_name=_("Datei"),
    )
    
    expire_date = models.DateTimeField(
        verbose_name=_("Ausfallsdatum"),
        blank=True,
        null=True
    )
    
    @hook(BEFORE_UPDATE, when="send_one")
    def _hook_check_if_is_sent(self):
        if self.is_online:
            raise ValueError(_(
                "Die Datei wurde bereits gesendet. Das Sendedatum kann nicht mehr geändert werden"
            ))
