import os
from datetime import datetime
from pathlib import Path
from typing import *

__all__ = [
    "get_file_dates", "set_file_dates"
]


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
