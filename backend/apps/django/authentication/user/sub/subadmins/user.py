import secrets
import string
from typing import Optional

from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_hint import RequestType

from ...models import User

__all__ = [
    "UserAdmin",
]


@admin.register(User)
class UserAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "email", "id", "is_active", "!..."],
        "advanced": ["last_login", "user_permissions", "is_staff", "confirmation_key"]
    }
    list_display = ["email", "id", "is_active", "is_confirmed"]
    list_filter = ["is_active"]
    readonly_fields = ["confirmation_key", "last_login", "first_name", "last_name", "email"]
    filter_horizontal = ["user_permissions"]
    
    def has_change_permissions_permission(self, request: RequestType, obj: User) -> bool:
        return request.user.has_perm("authentication.change_user_permissions") and obj != request.user
    
    def get_readonly_fields(self, request: RequestType, obj: Optional[User] = None) -> list:
        if obj:
            # Required readonly
            readonly_list = ["confirmation_key", "last_login", "first_name", "last_name", "email", "is_active", "id"]
            
            can_change_permissions = self.has_change_permissions_permission(request, obj)
            
            if not can_change_permissions or obj.has_perm("authentication.change_user_permissions"):
                readonly_list += ["user_permissions", "is_staff"]
            
            return readonly_list
        return ["id", "confirmation_key", "last_login"]
    
    def save_model(self, request: RequestType, obj: User, form, change):
        if not change:
            # Automatically confirm email
            obj._dont_send_confirmation_mail = True
            response = super().save_model(request, obj, form, change)
            delattr(obj, "_dont_send_confirmation_mail")
            obj.confirm_email(obj.confirmation_key)
            
            # Set random password
            password = "".join(
                secrets.choice(string.ascii_letters + string.digits)
                for _ in range(20)
            )
            obj.set_password(password)
            obj.save()
            
            return response
        else:
            return super().save_model(request, obj, form, change)
