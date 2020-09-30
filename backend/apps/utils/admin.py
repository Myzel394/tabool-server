from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.admin import BaseAdminMixinsMixin
from django_common_utils.libraries.fieldsets.sections import FieldsetList, Sections

__all__ = [
    "DefaultAdminInlineMixin"
]


class DefaultAdminInlineMixin(BaseAdminMixinsMixin, admin.TabularInline):
    extra = 0
    min_num = 0
    
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
                classes=["collapse", ],
                description=_("Extra-Einstellungen"),
                name="advanced",
                fields=[]
            ),
            FieldsetList(
                order=2,
                appearance=None,
                classes=["collapse", ],
                name="created",
                description=_("Einstellung sichtbar nach Erstellung des Objekts."),
                fields=[
                    "id"
                ]
            )
        ])
