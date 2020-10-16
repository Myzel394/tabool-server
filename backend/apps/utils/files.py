import os
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.db.models import Model
from django_hint import *
from magic import Magic
from PIL import Image

from constants import dates

__all__ = [
    "build_path", "get_file_dates", "set_file_dates", "remove_private_data", "privatize_file"
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
           + "/".join(str(x) for x in [now.year, now.month, now.day, now.hour]) \
           + build_str("", suffix, "/") + filename
    
    return path


def get_file_dates(path: Union[Path, str]) -> dict:
    return {
        "modified_at": datetime.fromtimestamp(os.path.getmtime(str(path))),
        "accessed_at": datetime.fromtimestamp(os.path.getatime(str(path))),
    }


def set_file_dates(
        path: Union[Path, str],
        *,
        modified_at: Optional[datetime] = None,
        accessed_at: Optional[datetime] = None
) -> None:
    os.utime(str(path), (accessed_at.timestamp(), modified_at.timestamp()))


def remove_private_data(path: Union[Path, str]):
    path_str = str(path)
    m = Magic(mime=True)
    
    mime_type = m.from_file(path_str)
    
    if mime_type.startswith("image"):
        # TODO: Find type
        with Image.open(path_str) as image:
            data = image.getdata()
            mode = image.mode
            size = image.size
        
        image_without_exif = Image.new(mode, size)
        image_without_exif.putdata(data)
        image_without_exif.save(path_str)


def privatize_file(file: str):
    remove_private_data(file)
    set_file_dates(
        file,
        modified_at=dates.DEFAULT_TRACE_DATE,
        accessed_at=dates.DEFAULT_TRACE_DATE
    )
