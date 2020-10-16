from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Classtest

__all__ = [
    "Classtest"
]


@admin.register(Classtest)
class ClassTestAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["targeted_date", "course", "room", "!..."],
        "extra": ["information", "created_at", "!..."]
    }
    list_display = ["__str__", "targeted_date", "course"]
    search_fields = ["information"]
    list_filter = ["course__subject", "room"]
    date_hierarchy = "targeted_date"
    inlines = [
        CourseAdminInline, RoomAdminInline
    ]
