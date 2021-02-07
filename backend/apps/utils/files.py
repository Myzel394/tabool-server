from datetime import datetime

from django.conf import settings
from django.db.models import Model
from django_hint import *

__all__ = [
    "build_path"
]


def build_str(prefix: str, string: str, suffix: str) -> str:
    if not string.startswith(prefix):
        string = prefix + string
    if not string.endswith(suffix):
        string += suffix
    
    return string


def build_path(
        filename: str,
        prefix: str = "",
        suffix: str = "",
        *,
        instance: Optional[Model] = None,
        is_private: bool = False,
) -> str:
    now = datetime.now()
    access_folder = settings.PRIVATE_STORAGE_FOLDER if is_private else settings.PUBLIC_STORAGE_FOLDER
    
    if instance:
        prefix += getattr(instance, "folder_name", instance.id)
    
    path = build_str("", access_folder, "/") \
           + build_str("", prefix, "/") \
           + "/".join(str(x) for x in [now.year, now.month, now.day]) \
           + build_str("", suffix, "/") + filename
    
    return path
