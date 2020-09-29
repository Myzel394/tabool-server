from django.contrib import admin

from ..models import Room


class RoomAdmin(admin.TabularInline):
    model = Room
    extra = 0
    min_num = 0
    fieldsets = {
        "", {
            "fields": ["place"]
        },
        "created", {
            "fields": ["id"]
        }
    }
    
    # TODO: Change django_common_utils!

    


