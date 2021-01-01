from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import *

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from ...models import Room, RoomScoosoData

__all__ = [
    "RoomAdmin"
]


class RoomScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = RoomScoosoData
    fieldset_fields = {
        "default": ["code", "!..."]
    }
    readonly_fields = ["code", "scooso_id"]


@admin.register(Room)
class RoomAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["place"]
    }
    inlines = [RoomScoosoDataAdminInline]
    search_fields = ["place"]
