import random
import string
from typing import *

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, hook, LifecycleModel
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from ..helpers import send_email_verification
from ..querysets import UserQuerySet

if TYPE_CHECKING:
    from ..querysets import UserPaymentQuerySet

__all__ = [
    "User"
]


class User(AbstractUser, SimpleEmailConfirmationUserMixin, LifecycleModel):
    id = models.CharField(
        verbose_name=_("ID"),
        blank=True,
        editable=False,
        max_length=6 + 4,
        primary_key=True,
    )  # type: str
    
    email = models.EmailField(
        verbose_name=_("Email-Adresse"),
        unique=True,
    )  # type: str
    
    username = None
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserQuerySet()
    
    def __str__(self):
        return _("{first_name} {last_name} (ID: {id})").format(
            first_name=self.first_name,
            last_name=self.last_name,
            id=self.id
        )
    
    @hook(BEFORE_CREATE)
    def _hook_create_id(self):
        while True:
            random_id = "".join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=6
                )
            ) + "@" + "".join(
                random.choices(
                    string.digits,
                    k=4
                )
            )
            
            if not self.__class__.objects.only("id").filter(id=random_id).exists():
                break
        
        self.id = random_id
    
    @hook(AFTER_CREATE)
    def _hook_send_mail(self):
        send_email_verification(self)
    
    @property
    def payments(self) -> "UserPaymentQuerySet":
        return self.userpayment_set.all()
