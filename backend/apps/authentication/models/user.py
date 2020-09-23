import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import BEFORE_CREATE, hook, LifecycleModel

from apps.authentication.sub.subquerysets.user import UserQuerySet

__all__ = [
    "User"
]


# TODO: Admin pages hinzufüen!


class User(AbstractUser, LifecycleModel):
    id = models.CharField(
        verbose_name=_("ID"),
        blank=True,
        editable=False,
        max_length=6 + 4,
        primary_key=True,
    )
    email = models.EmailField(
        verbose_name=_("Email-Adresse"),
        unique=True,
    )
    
    username = None
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserQuerySet()
    
    def __str__(self):
        return self.email
    
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
