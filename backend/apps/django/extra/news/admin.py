from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import *

from .models import News

__all__ = [
    "NewsAdmin"
]


@admin.register(News)
class NewsAdmin(DefaultAdminMixin):
    mixins = [EditCreationDateAdminFieldsetMixin]
    fieldset_fields = {
        "default": ["title", "html", "author", "!..."]
    }
