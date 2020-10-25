from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin
from django_hint import RequestType
from django_object_actions import DjangoObjectActions

from apps.django.extra.scooso_scraper.sub.subjobs import fetch_timetable
from ...models import Student, User

__all__ = [
    "UserAdmin"
]


class StudentAdminInline(admin.StackedInline):
    model = Student
    fields = ["main_teacher", "class_number"]
    min_num = 0
    max_num = 0
    autocomplete_fields = ["main_teacher"]


@admin.register(User)
class UserAdmin(DjangoObjectActions, DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "email", "id", "is_active", "!..."],
        "advanced": ["confirmation_key", "last_login"]
    }
    list_display = ["email", "id", "is_active", "is_confirmed"]
    list_filter = ["is_active"]
    readonly_fields = ["confirmation_key", "last_login"]
    inlines = [StudentAdminInline]
    change_actions = ("fetch_timetable",)
    
    def fetch_timetable(self, request: RequestType, obj: User):
        if hasattr(obj, "scoosodata"):
            fetch_timetable(obj)
            messages.success(request, _("Scooso-Stundenplan von {user} wurde geladen.").format(
                user=obj
            ))
        else:
            messages.error(request, _("{user} hat noch keine Scooso-Daten angegeben.").format(
                user=obj
            ))
    
    fetch_timetable.label = _("Scooso-Stundenplan laden")
