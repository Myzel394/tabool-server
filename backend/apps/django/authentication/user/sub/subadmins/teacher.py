from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Teacher

__all__ = [
    "TeacherAdmin"
]


@admin.register(Teacher)
class TeacherAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "short_name", "email", "gender", "id", "!..."],
        "creation": ["id", "!..."]
    }
    # TODO: Add first_name and last_name
    list_display = ["short_name"]
    readonly_fields = ["email"]
    search_fields = ["user__first_name", "user__last_name", "short_name"]
