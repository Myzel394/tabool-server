import secrets
import string
from typing import Optional

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_hint import RequestType

from ...models import User

__all__ = [
    "UserAdmin",
]


@admin.register(User)
class UserAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "email", "gender", "is_active", "!..."],
        "advanced": ["last_login", "user_permissions", "is_staff", "confirmation_key", "id"]
    }
    list_display = ["email", "first_name", "last_name", "get_user_type", "is_active", "is_confirmed"]
    list_filter = ["is_active", "is_staff", "gender"]
    readonly_fields = ["confirmation_key", "last_login", "first_name", "last_name", "email"]
    filter_horizontal = ["user_permissions"]

    @staticmethod
    def has_change_permissions_permission(request: RequestType, obj: User) -> bool:
        return request.user.has_perm("authentication.change_user_permissions") and obj != request.user

    def get_readonly_fields(self, request: Optional[RequestType] = None, obj: Optional[User] = None) -> list:
        if obj and request:
            # Required readonly
            readonly_list = ["confirmation_key", "last_login", "first_name", "last_name", "email", "is_active", "id"]

            can_change_permissions = self.has_change_permissions_permission(request, obj)

            if not can_change_permissions or obj.has_perm("authentication.change_user_permissions"):
                readonly_list += ["user_permissions", "is_staff"]

            return readonly_list
        return ["id", "confirmation_key", "last_login"]

    def save_model(self, request: RequestType, obj: User, form, change):
        if change:
            super().save_model(request, obj, form, change)
        else:
            # Automatically confirm email
            obj._dont_send_confirmation_mail = True  # skipcq: PYL-W0212
            super().save_model(request, obj, form, change)
            delattr(obj, "_dont_send_confirmation_mail")
            obj.confirm_email(obj.confirmation_key)

            # Set random password
            password = "".join(
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(20)
            )
            obj.set_password(password)
            obj.save()

    @staticmethod
    def get_user_type(instance: User):
        try:
            return instance.user_type
        except TypeError:
            return _("Unbekannt")
