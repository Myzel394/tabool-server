from datetime import datetime

from django.conf import settings
from django.db.models import Model
from django_hint import *

__all__ = [
    "build_path"
]


def build_path(
        filename: str,
        prefix: str = "",
        suffix: str = "",
        *,
        instance: Optional[Model] = None
) -> str:
    now = datetime.now()
    
    if instance:
        prefix += "/" + getattr(instance, "folder_name", instance.id)
    
    return settings.MEDIA_ROOT.joinpath(
        prefix + "/" +
        "/".join(str(x) for x in [now.year, now.month, now.day, now.hour]) +
        suffix + "/" +
        filename
    )
