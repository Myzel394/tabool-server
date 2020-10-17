from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import *

from ...models import Subject

__all__ = [
    "SubjectAdmin"
]


@admin.register(Subject)
class SubjectAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["name", "short_name", "!..."],
        "extra": ["color", "!..."]
    }
