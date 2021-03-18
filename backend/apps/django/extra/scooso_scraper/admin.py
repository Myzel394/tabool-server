from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from apps.django.extra.scooso_scraper.models import ScoosoRequest


@admin.register(ScoosoRequest)
class ScoosoRequestAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["name", "created_at", "response"]
    }
    
    list_filter = ["name"]
    list_display = ["name", "created_at"]
    date_hierarchy = "created_at"
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
