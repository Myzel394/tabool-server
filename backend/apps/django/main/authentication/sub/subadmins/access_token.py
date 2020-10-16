from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import AccessToken

__all__ = [
    "AccessTokenAdmin"
]


@admin.register(AccessToken)
class AccessTokenAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["user", "token", "created_at", "!..."]
    }
    readonly_fields = [
        "user", "token", "created_at"
    ]
    list_display = ["user", "created_at"]
    date_hierarchy = "created_at"
