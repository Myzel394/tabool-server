import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, hook, LifecycleModel
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from .preference import Preference
from ..helpers import send_email_verification
from ..querysets import UserManager, UserQuerySet

__all__ = [
    "User"
]


# TODO: Add student data!
class User(AbstractUser, SimpleEmailConfirmationUserMixin, LifecycleModel):
    class Meta:
        permissions = (
            ("change_user_permissions", _("Kann Benutzer-Berechtigungen verändern")),
        )
    
    id = models.CharField(
        verbose_name=_("ID"),
        blank=True,
        editable=False,
        max_length=6 + 1 + 4,
        primary_key=True,
    )  # type: str
    
    email = models.EmailField(
        verbose_name=_("Email-Adresse"),
        unique=True,
    )  # type: str
    
    has_filled_out_data = models.BooleanField(
        default=False,
        verbose_name=_("Daten ausgefüllt")
    )  # type: bool
    
    load_scooso_data = models.BooleanField(
        default=True,
        verbose_name=_("Scooso-Daten laden")
    )
    
    username = None
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager.from_queryset(UserQuerySet)()
    
    def __str__(self):
        return _("{first_name} {last_name}, {email_part} (ID: {id})").format(
            first_name=self.first_name,
            last_name=self.last_name,
            id=self.id,
            email_part=self.email.split("@", 1)[0]
        )
    
    @hook(BEFORE_CREATE)
    def _hook_create_id(self):
        while True:
            first_id_part = "".join(
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(6)
            )
            second_id_part = "".join(
                secrets.choice(string.digits)
                for _ in range(4)
            )
            user_id = f"{first_id_part}@{second_id_part}"
            
            if not self.__class__.objects.only("id").filter(id=user_id).exists():
                break
        
        self.id = user_id
    
    @hook(AFTER_CREATE)
    def _hook_send_mail(self):
        send_email_verification(self)
    
    @hook(AFTER_CREATE)
    def _hook_create_preference(self):
        Preference.objects.create(
            user=self
        )
    
    @property
    def is_scooso_data_valid(self) -> bool:
        return self.first_name is not None
