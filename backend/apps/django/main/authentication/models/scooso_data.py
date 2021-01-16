from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_lifecycle import LifecycleModel
from fernet_fields import EncryptedCharField

from apps.django.extra.scooso_scraper.scrapers.request import Request
from ..notifications import push_scooso_data_invalid
from ..public import model_names
from ..querysets import ScoosoDataQuerySet

__all__ = [
    "ScoosoData"
]


class ScoosoData(RandomIDMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.SCOOSO_DATA
        verbose_name_plural = model_names.SCOOSO_DATA_PLURAL
        ordering = ("user",)
    
    objects = ScoosoDataQuerySet()
    
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name=model_names.USER,
    )
    
    scooso_id = models.CharField(
        max_length=127,
        verbose_name=_("Scooso-Id"),
    )
    
    username = EncryptedCharField(
        max_length=127,
        verbose_name=_("Scooso-Benutzername"),
        help_text=_("Der Scooso-Benutername wird verschlüsselt gespeichert"),
    )
    
    password = EncryptedCharField(
        max_length=127,
        verbose_name=_("Scooso-Passwort"),
        help_text=_("Das Scooso-Password wird verschlüsselt gespeichert"),
    )
    
    def fetch_user_data(self):
        user = self.user
        try:
            scraper = Request(self.username, self.password)
            data = scraper.login(login_attempts=2)
            first_name = data["first_name"]
            last_name = data["last_name"]
            scooso_id = data["id"]
        except:
            push_scooso_data_invalid(self.user)
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.scooso_id = scooso_id
            user.save()
    
    def __str__(self):
        return str(self.user)
