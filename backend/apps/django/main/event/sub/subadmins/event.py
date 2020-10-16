from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Event

__all__ = [
    "EventAdmin"
]


@admin.register(Event)
class EventAdmin(DefaultAdminMixin):
    list_display = ["title", "room"]
    list_filter = ["room"]
    fieldset_fields = {
        "default": ["title", "start_datetime", "end_datetime", "room", "!..."]
    }
    date_hierarchy = "start_datetime"
    search_fields = ["title"]
    inlines = [
        RoomAdminInline
    ]
