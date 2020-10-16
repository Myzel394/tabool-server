from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin
from django_common_utils.libraries.models.mixins.common import RandomIDMixin

from ..querysets import UserPaymentQuerySet

if TYPE_CHECKING:
    from ..public import *

__all__ = [
    "UserPayment"
]


class UserPayment(RandomIDMixin, CreationDateMixin):
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
    
    def is_user_owner(self, user: "USER") -> bool:
        return user == self.user
