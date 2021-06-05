from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from ...models import Classbook

__all__ = [
    "ClassbookAdmin"
]


@admin.register(Classbook)
class ClassbookAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["online_content", "presence_content", "video_conference_link"],
        "advanced": ["lesson", "lesson_date"]
    }
    list_display = ["__str__", "has_video_conference"]
    
    @staticmethod
    def has_video_conference(instance: Classbook) -> bool:
        return instance.video_conference_link != "" and instance.video_conference_link is not None
    
    has_video_conference.short_description = _("Videokonferenz")
    has_video_conference.boolean = True
