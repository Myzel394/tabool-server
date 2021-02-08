from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Teacher

__all__ = [
    "TeacherAdmin"
]


@admin.register(Teacher)
class TeacherAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["short_name", "!..."],
        "creation": ["id", "!..."]
    }
    # TODO: Add first_name and last_name
    list_display = ["short_name"]
    search_fields = ["user__first_name", "user__last_name", "short_name"]
