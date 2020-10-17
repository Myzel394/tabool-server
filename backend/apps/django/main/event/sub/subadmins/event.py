from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.django.utils.admins import build_date
from ...models import Event

__all__ = [
    "EventAdmin"
]


@admin.register(Event)
class EventAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["title", "start_datetime", "end_datetime", "room", "!..."]
    }
    list_display = ["title", "date", "room"]
    list_filter = ["room"]
    date_hierarchy = "start_datetime"
    autocomplete_fields = ["room"]
    
    def date(self, instance: Event):
        return build_date(instance.start_datetime, instance.end_datetime)
    
    date.short_description = _("Datum")
