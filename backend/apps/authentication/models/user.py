import random
import re
import string

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django_lifecycle import BEFORE_CREATE, hook, LifecycleModel


__all__ = [
    "User"
]


# TODO: Admin pages hinzufüen!
from apps.authentication.sub.subquerysets.user import UserQuerySet


class User(AbstractUser, LifecycleModel):
    id = models.CharField(
        verbose_name=_("ID"),
        blank=True,
        editable=False,
    )
    
    username = None
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserQuerySet.as_manager()
    
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
            
            if self.objects.only("id").get(id=random_id):
                break
        
        self.id = random_id

