from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import CreationDateAdminFieldsetMixin, DefaultAdminMixin
from simple_history.admin import SimpleHistoryAdmin

from ...models import Classtest

__all__ = [
    "ClasstestAdmin"
]


@admin.register(Classtest)
class ClasstestAdmin(DefaultAdminMixin, SimpleHistoryAdmin):
    fieldset_fields = {
        "default": ["course", "room", "targeted_date", "information", "!..."]
    }
    list_display = ["course", "room", "targeted_date"]
    list_filter = ["course", "course", "course__subject"]
    search_fields = ["information", "course", "targeted_date"]
    autocomplete_fields = ["course", "room"]
    mixins = [CreationDateAdminFieldsetMixin]
