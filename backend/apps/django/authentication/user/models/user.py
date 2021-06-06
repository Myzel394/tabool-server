import secrets
import string
from typing import *

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, hook, LifecycleModel
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from apps.utils.texts import max_length_from_choices
from .preference import Preference
from ..choices import GenderChoices
from ..constants import STUDENT, TEACHER
from ..helpers import send_email_verification
from ..querysets import UserManager, UserQuerySet

if TYPE_CHECKING:
    from . import Student, Teacher

__all__ = [
    "User"
]


class User(AbstractUser, SimpleEmailConfirmationUserMixin, LifecycleModel):
    class Meta:
        permissions = (
            ("change_user_permissions", _("Kann Benutzer-Berechtigungen verändern")),
        )
        ordering = ("first_name", "last_name")

    student: "Student"
    teacher: "Teacher"

    id = models.CharField(
        verbose_name=_("ID"),
        blank=True,
        editable=False,
        max_length=10 + 1 + 8,
        primary_key=True,
    )  # type: str

    email = models.EmailField(
        verbose_name=_("Email-Adresse"),
        unique=True,
    )  # type: str

    gender = models.CharField(
        choices=GenderChoices.choices,
        verbose_name=_("Geschlecht"),
        default=GenderChoices.DIVERSE,
        max_length=max_length_from_choices(GenderChoices.choices)
    )  # type: str

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

    @property
    def user_type(self) -> Union[STUDENT, TEACHER]:
        try:
            self.student
        except ObjectDoesNotExist:
            try:
                self.teacher
            except ObjectDoesNotExist:
                raise TypeError("User hasn't filled in his data.")
            else:
                return TEACHER
        else:
            return STUDENT

    @property
    def is_teacher(self) -> bool:
        return self.user_type == TEACHER

    @property
    def is_student(self) -> bool:
        return self.user_type == STUDENT

    @hook(BEFORE_CREATE)
    def _hook_create_id(self):
        while True:
            first_id_part = "".join(
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(10)
            )
            second_id_part = "".join(
                secrets.choice(string.digits)
                for _ in range(8)
            )
            user_id = f"{first_id_part}@{second_id_part}"

            if not self.__class__.objects.only("id").filter(id=user_id).exists():
                break

        self.id = user_id

    @hook(AFTER_CREATE)
    def _hook_send_mail(self):
        if getattr(self, "_dont_send_confirmation_mail", False):
            return

        send_email_verification(self)

    @hook(AFTER_CREATE)
    def _hook_create_preference(self):
        Preference.objects.create(
            user=self
        )
