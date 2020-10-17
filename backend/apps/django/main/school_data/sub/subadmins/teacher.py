from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import *

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from ...models import Teacher, TeacherScoosoData

__all__ = [
    "TeacherAdmin"
]


class TeacherScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = TeacherScoosoData
    fieldset_fields = {
        "default": ["code", "!..."]
    }


@admin.register(Teacher)
class TeacherAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "short_name", "email", "!..."],
    }
    inlines = [TeacherScoosoDataAdminInline]
    list_display = ["short_name", "first_name", "last_name"]
    search_fields = ["short_name", "first_name", "last_name"]
