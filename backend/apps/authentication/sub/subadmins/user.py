from django.contrib import admin
from django_common_utils.libraries.fieldsets import DefaultAdminMixin

from ...models import User, AccessToken, UserPayment


__all__ = [
    "UserAdmin"
]


class UserAccessTokenAdmin(admin.TabularInline):
    model = AccessToken
    fieldsets = [
        ["", {
            "fields": ["token", "created_at"]
        }]
    ]
    readonly_fields = [
        "token", "created_at"
    ]
    extra = 0
    max_num = 1
    can_delete = False


class UserUserPaymentAdmin(admin.TabularInline):
    model = UserPayment
    fieldsets = [
        ["", {
            "fields": ["paid_at"]
        }]
    ]
    extra = 0


@admin.register(User)
class UserAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "email", "!..."],
        "extra": ["is_staff", "is_active", "date_joined", "id", "!..."],
        "created": []
    }
    inlines = [UserAccessTokenAdmin, UserUserPaymentAdmin]
    search_fields = ["first_name", "last_name", "email", "id"]
    list_display = ["first_name", "last_name", "email", "id"]
    list_filter = ["is_active"]
    date_hierarchy = "date_joined"
