from typing import *

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from ...models import User

__all__ = [
    "UserManager", "UserQuerySet"
]


class UserManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email: str) -> str:
        return email.lower()

    def create_user(self, email: str, password: str, **extra_fields) -> "User":
        if not email:
            raise ValueError(_("Email nicht angegeben."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_staff=True and is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class UserQuerySet(models.QuerySet):
    def active_users(self) -> "UserQuerySet":
        return self.only("is_active") \
            .prefetch_related("email_address_set") \
            .filter(is_active=True, email_address_set__confirmed_at__isnull=False)
