from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from apps.django.main.school_data.public import model_names as school_names
from ...models import Material, MaterialScoosoData

__all__ = [
    "MaterialAdmin"
]


class MaterialScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = MaterialScoosoData
    fieldset_fields = {
        "default": ["scooso_id", "owner_id"]
    }


@admin.register(Material)
class MaterialAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["lesson", "file", "name", "!..."]
    }
    list_display = ["__str__", "added_at", "subject"]
    list_filter = ["lesson__lesson_data__course__subject"]
    autocomplete_fields = ["lesson"]
    date_hierarchy = "added_at"
    inlines = [MaterialScoosoDataAdminInline]
    
    def subject(self, instance: Material):
        return instance.lesson.lesson_data.course.subject
    
    subject.short_description = school_names.SUBJECT
