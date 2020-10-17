from django.contrib import admin
from django_common_utils.libraries.fieldsets.admin import BaseAdminMixinsMixin
from django_common_utils.libraries.fieldsets.sections import FieldsetList, Sections

__all__ = [
    "ScoosoDataAdminInlineMixin"
]


class ScoosoDataAdminInlineMixin(BaseAdminMixinsMixin, admin.StackedInline):
    max_num = 1
    min_num = 1
    
    def get_section(self) -> Sections:
        return Sections([
            FieldsetList(
                order=0,
                appearance=None,
                name="default",
                fields=[]
            ),
            FieldsetList(
                order=1,
                appearance=None,
                name="extra",
                fields=[],
            )
        ])
    
    def has_delete_permission(self, request, obj=None):
        return None
