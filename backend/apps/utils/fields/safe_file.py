import mimetypes
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import *

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from secure_file_detection import detector
from secure_file_detection.constants import SUPPORTED_MIMETYPES
from secure_file_detection.exceptions import *

__all__ = [
    "SafeFileField"
]


class MimetypeValidator:
    NOT_SUPPORTED_ERROR_MESSAGE = _(
        "Dieses Dateiformat wird aus Sicherheitsgründen nicht unterstützt. Du musst die Datei selber auf Scooso "
        "hochladen."
    )
    MANIPULATED_FILE_ERROR_MESSAGE = _(
        "Diese Datei scheint manipuliert zu sein. Wenn du kein Hacker bist, solltest du die Datei am besten löschen."
    )
    
    def __init__(self, mimetypes):
        self.mimetypes = mimetypes
    
    def __call__(self, file: InMemoryUploadedFile):
        with self.create_temp_path(file.name) as path:
            data = file.read()
            path.write_bytes(data)
            
            mime_type = self.get_mimetype(path)
            new_path = self.rename_file(path, mime_type)
        
        return new_path
    
    @staticmethod
    @contextmanager
    def create_temp_path(suffix: str = "") -> ContextManager[Path]:
        temp_path = Path(f"/tmp/tabool/safe_file_temp_{datetime.now().strftime('%Y%m%D.%H:%M:%S')}{suffix}")
        temp_path.parent.mkdir(exist_ok=True, parents=True)
        temp_path.touch(exist_ok=True)
        
        try:
            yield temp_path
        finally:
            temp_path.unlink(missing_ok=True)
    
    @classmethod
    def get_mimetype(cls, path: Path) -> str:
        try:
            mime_type = detector.detect_true_type(path)
        except MimeTypeNotSupported:
            raise ValidationError(cls.NOT_SUPPORTED_ERROR_MESSAGE, code="mimetype_not_supported")
        except (MimeTypeNotDetectable, ManipulatedFileError):
            raise ValidationError(cls.MANIPULATED_FILE_ERROR_MESSAGE, code="manipulated_file")
        
        return mime_type
    
    @classmethod
    def rename_file(cls, path: Path, mime_type: str) -> Path:
        extension = mimetypes.guess_extension(mime_type)
        
        if extension is None:
            raise ValidationError(cls.NOT_SUPPORTED_ERROR_MESSAGE, code="mimetype_not_supported")
        
        path.rename(path.with_suffix(extension))
        return path


class SafeFileField(models.FileField):
    def __init__(self, valid_mimetypes: Optional[Iterable[str]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        valid_mimetypes = valid_mimetypes or SUPPORTED_MIMETYPES
        self.validators.append(MimetypeValidator(valid_mimetypes))
