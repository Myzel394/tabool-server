from django.db import models
from django.utils.translation import gettext_lazy as _

from ..querysets import UserPaymentQuerySet

__all__ = [
    "UserPayment"
]


class UserPayment(models.Model):
    class Meta:
        verbose_name = _("Benutzer-Bezahlung")
        verbose_name_plural = _("Benutzer-Bezahlungen")
        ordering = ("user",)
    
    objects = UserPaymentQuerySet()
    
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
    )
    
    paid_at = models.DateTimeField(
        verbose_name=_("Gezahlt um"),
        blank=True,
        null=True
    )
    
    @property
    def has_paid(self) -> bool:
        return self.paid_at is not None
