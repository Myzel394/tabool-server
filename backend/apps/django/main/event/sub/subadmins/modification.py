from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import model_verbose

from apps.django.utils.admins import build_date
from ...models import Modification

__all__ = [
    "ModificationAdmin"
]


@admin.register(Modification)
class ModificationAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["course", "new_room", "new_subject", "new_teacher", "start_datetime", "end_datetime",
                    "information", "modification_type"]
    }
    list_display = ["__str__", "course", "modifications", "date"]
    list_filter = ["course", "course__subject"]
    autocomplete_fields = ["new_room", "new_subject", "new_teacher"]
    search_fields = ["information", "modification_type", "course"]
    
    def modifications(self, instance: Modification):
        elements = []
        
        if instance.new_subject:
            elements.append(instance.new_subject)
        if instance.new_teacher:
            elements.append(instance.new_teacher)
        if instance.new_room:
            elements.append(instance.new_room)
        
        return "; ".join(
            f"+[{model_verbose(element)}: {element}]"
            for element in elements
        )
    
    modifications.short_description = _("Veränderungen")
    
    def date(self, instance: Modification):
        return build_date(instance.start_datetime, instance.end_datetime)
