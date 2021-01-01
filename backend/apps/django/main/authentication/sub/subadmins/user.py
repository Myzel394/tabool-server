from typing import Optional

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
    readonly_fields = ["main_teacher", "class_number"]


@admin.register(User)
class UserAdmin(DjangoObjectActions, DefaultAdminMixin):
    fieldset_fields = {
        "default": ["first_name", "last_name", "email", "id", "is_active", "!..."],
        "advanced": ["confirmation_key", "last_login", "user_permissions", "is_staff"]
    }
    list_display = ["email", "id", "is_active", "is_confirmed"]
    list_filter = ["is_active"]
    readonly_fields = ["confirmation_key", "last_login", "first_name", "last_name", "email"]
    inlines = [StudentAdminInline]
    change_actions = ("fetch_timetable",)
    filter_horizontal = ["user_permissions"]
    
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
    
    def has_change_permissions_permission(self, request: RequestType, obj: User) -> bool:
        return request.user.has_perm("authentication.change_user_permissions") and obj != request.user
    
    def get_readonly_fields(self, request: Optional[RequestType] = None, obj: Optional[User] = None) -> list:
        # Required readonly
        readonly_list = ["confirmation_key", "last_login", "first_name", "last_name", "email", "is_active", "id"]
        
        can_change_permissions = request and obj and self.has_change_permissions_permission(request, obj)
        
        if not can_change_permissions:
            readonly_list += ["user_permissions", "is_staff"]
        
        return readonly_list
