from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin
from django_common_utils.libraries.models.mixins.common import RandomIDMixin

from ..public import model_names
from ..querysets import UserPaymentQuerySet

if TYPE_CHECKING:
    from ..public import *
    from . import User

__all__ = [
    "UserPayment"
]


class UserPayment(RandomIDMixin, CreationDateMixin):
    class Meta:
        verbose_name = model_names.USER_PAYMENT
        verbose_name_plural = model_names.USER_PAYMENT_PLURAL
        ordering = ("user",)
    
    objects = UserPaymentQuerySet()
    
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        verbose_name=model_names.USER
    )  # type: User
    
    paid_at = models.DateTimeField(
        verbose_name=_("Gezahlt um"),
        blank=True,
        null=True
    )  # type: datetime
    
    @property
    def has_paid(self) -> bool:
        return self.paid_at is not None
    
    def is_user_owner(self, user: "USER") -> bool:
        return user == self.user
