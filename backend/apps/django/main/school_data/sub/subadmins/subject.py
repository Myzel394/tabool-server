from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import *

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from ...models import Subject, SubjectScoosoData

__all__ = [
    "SubjectAdmin"
]


class SubjectScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = SubjectScoosoData
    fieldset_fields = {
        "default": ["code", "!..."]
    }
    readonly_fields = ["code", "scooso_id"]


@admin.register(Subject)
class SubjectAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["name", "short_name"],
    }
    inlines = [SubjectScoosoDataAdminInline]
    list_display = ["name", "short_name"]
    search_fields = ["name", "short_name"]
