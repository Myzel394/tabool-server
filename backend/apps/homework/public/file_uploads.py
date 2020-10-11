from typing import *

from apps.utils.files import build_path

if TYPE_CHECKING:
    from ..models import Material, Submission

__all__ = [
    "build_material_upload_to", "build_submission_upload_to"
]


def build_material_upload_to(instance: "Material", filename: str, *args, **kwargs) -> str:
    return build_path(filename, "scooso_downloads/material/", instance=instance)


def build_submission_upload_to(instance: "Submission", filename: str, *args, **kwargs) -> str:
    return build_path(filename, "scooso_uploads/submission/", instance=instance)
