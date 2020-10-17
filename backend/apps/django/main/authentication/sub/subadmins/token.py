from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import AccessToken

__all__ = [
    "TokenAdmin"
]


# TODO: Rename AccessToken -> Token
@admin.register(AccessToken)
class TokenAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["user", "token", "!..."]
    }
    readonly_fields = ["user", "token"]
    list_display = ["user", "created_at"]
