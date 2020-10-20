from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Token

__all__ = [
    "TokenAdmin"
]

from ...public.model_names import USER


@admin.register(Token)
class TokenAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["user", "token", "!..."]
    }
    readonly_fields = ["user", "token"]
    list_display = ["get_user", "created_at"]
    
    def get_user(self, instance: Token):
        return instance.user
    
    get_user.empty_value_display = _("[Kein Benutzer]")
    get_user.short_description = USER
