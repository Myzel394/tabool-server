from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Subject

__all__ = [
    "SubjectAdmin"
]


@admin.register(Subject)
class SubjectAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["name", "short_name", "!..."],
        "created": ["id", "!..."]
    }
    list_display = ["name", "short_name"]
    search_fields = ["name", "short_name"]
