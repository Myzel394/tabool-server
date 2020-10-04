import os
from datetime import date, datetime
from pathlib import Path
from typing import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from secure_file_detection import detector

if TYPE_CHECKING:
    from .models import Material

__all__ = [
    "build_material_path", "validate_material_file"
]


def build_material_path(instance: "Material", filename: str) -> str:
    today = date.today()
    
    return f"uploads/materials/{instance.lesson.lesson_data.course.name}" \
           f"/{today.year}/{today.month}/{today.day}" \
           f"/{filename}"


def validate_material_file(data: bytes):
    def validate(path: Path):
        size = os.path.getsize(str(path))
        
        if size < (min_size := 100):
            raise ValidationError(_(
                f"Aus Sicherheitsgründen können keine Dateien hochgeladen werden, die kleiner als {min_size} bytes "
                f"groß "
                f"sind."
            ))
        
        if detector.is_file_manipulated(path):
            raise ValidationError(_(
                "Die Datei wurde abgelehnt, weil sie manipuliert wurde."
            ))
    
    path = Path().joinpath(f"tmp/{datetime.now().strftime('%d%m%Y_%H%M%S')}")
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    
    with path.open("wb") as file:
        file.write(data)
    
    try:
        validate(path)
    finally:
        path.unlink(missing_ok=True)
