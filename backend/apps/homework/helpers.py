import sys
from datetime import date, datetime
from pathlib import Path
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from secure_file_detection import detector

from . import constants

if TYPE_CHECKING:
    from .models import Material

__all__ = [
    "build_material_path", "validate_material_file"
]


def build_material_path(instance: "Material", filename: str) -> str:
    today = date.today()
    
    return f"uploads/materials/{instance.lesson.lesson_data.course.name}" \
           f"/{today.year}/{today.month}/{today.day}/{filename}"


def validate_material_file(data: bytes):
    def validate():
        size = sys.getsizeof(data)
        
        if size < constants.MIN_UPLOAD_SIZE:
            raise ValidationError(_(
                "Aus Sicherheitsgründen können keine Dateien hochgeladen werden, die kleiner als {min_size_bytes} "
                "bytes groß sind."
            ).format(
                min_size_bytes=constants.MIN_UPLOAD_SIZE
            ))
        elif size > constants.MAX_UPLOAD_SIZE:
            raise ValidationError(_(
                "Es können keine Dateien hochgeladen werden, die größer als {max_size_mib} MiB groß sind."
            ).format(
                max_size_mib=int(constants.MAX_UPLOAD_SIZE / 1000 / 1000)
            ))
        
        if detector.is_file_manipulated(path):
            raise ValidationError(_(
                "Die Datei wurde abgelehnt, weil sie manipuliert wurde."
            ))
    
    path = Path().joinpath(f"/tmp/{datetime.now().strftime('%d%m%Y_%H%M%S')}")
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    
    with path.open("wb") as file:
        file.write(data)
    
    try:
        validate()
    finally:
        path.unlink(missing_ok=True)
