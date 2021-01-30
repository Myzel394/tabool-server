from typing import *

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_common_utils.libraries.utils import model_verbose
from django_hint import RequestType

from ...models import Modification

__all__ = [
    "ModificationAdmin"
]


@admin.register(Modification)
class ModificationAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": [
            "lesson", "start_datetime", "end_datetime", "new_room", "new_subject", "new_teacher", "information",
            "modification_type"
        ]
    }
    list_display = ["__str__", "lesson", "modifications"]
    list_filter = ["lesson__course__subject", "modification_type"]
    autocomplete_fields = ["new_room", "new_subject", "new_teacher", "lesson"]
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
    
    def get_readonly_fields(self, request: Optional[RequestType] = None, obj: Optional[Modification] = None):
        if request.user.is_authenticated and request.user.is_superuser:
            return []
        
        if obj.from_scooso:
            return [
                "lesson", "start_datetime", "end_datetime", "room", "subject", "teacher", "information", "type"
            ]
        
        return []
