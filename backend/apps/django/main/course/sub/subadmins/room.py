from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Room

__all__ = [
    "RoomAdmin"
]


@admin.register(Room)
class RoomAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["place", "!..."],
        "created": ["id", "!..."]
    }
    list_display = ["__str__", "place"]
    search_fields = ["place"]
