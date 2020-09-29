from django.contrib import admin
from django_common_utils.libraries.fieldsets import DefaultAdminMixin

from ...models import Classtest

# TODO: Add subject user relation!


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
    


