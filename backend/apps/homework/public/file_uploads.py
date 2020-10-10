from typing import *

from apps.utils.files import build_path

if TYPE_CHECKING:
    from ..models import Material

__all__ = [
    "build_material_upload_to"
]


def build_material_upload_to(filename: str, instance: Optional["Material"] = None, *args, **kwargs) -> str:
    return build_path(filename, "uploads/material/", instance=instance)
