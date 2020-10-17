import mimetypes
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import *

from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext_lazy as _
from secure_file_detection import detector
from secure_file_detection.exceptions import *

from constants import upload_sizes

__all__ = [
    "SafeFileValidator"
]


class SafeFileValidator:
    TOO_SMALL_ERROR_MESSAGE = _(
        "Aus Sicherheitsgründen können keine Dateien hochgeladen werden, die kleiner als {min_size_bytes} bytes groß "
        "sind."
    )
    TOO_BIG_ERROR_MESSAGE = _(
        "Es können keine Dateien hochgeladen werden, die größer als {max_siz_mib} MiB groß sind."
    )
    MANIPULATED_FILE_ERROR_MESSAGE = _(
        "Die Datei scheint manipuliert zu sein. Sie kann daher zur Sicherheit nicht gespeichert werden."
    )
    NOT_SUPPORTED_ERROR_MESSAGE = _(
        "Dieses Dateiformat wird aus Sicherheitsgründen nicht unterstützt."
    )
    
    def __init__(
            self,
            mimetypes: Iterable[str],
            min_size: int = upload_sizes.MIN_UPLOAD_SIZE,
            max_size: int = upload_sizes.MAX_UPLOAD_SIZE
    ):
        self.mimetypes = mimetypes
        self.min_size = min_size
        self.max_size = max_size
    
    def __call__(self, file: FieldFile):
        size = file.size
        
        if size < self.min_size:
            raise ValidationError(self.TOO_SMALL_ERROR_MESSAGE.format(
                min_size_bytes=self.min_size
            ))
        elif size > self.max_size:
            raise ValidationError(self.TOO_BIG_ERROR_MESSAGE.format(
                max_siz_mib=int(self.max_size / 1000 / 1000)
            ))
        
        with self.create_temp_path(file.name, file.open("rb").read()) as path:
            mime_type = self.get_mimetype(path)
            new_path = self.rename_file(path, mime_type)
        
        return new_path
    
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
    
    @staticmethod
    @contextmanager
    def create_temp_path(name: str, data: bytes) -> ContextManager[Path]:
        temp_path = Path(f"/tmp/tabool/safe_file_temp_{datetime.now().strftime('%Y%m%D.%H:%M:%S')}{name}")
        temp_path.parent.mkdir(exist_ok=True, parents=True)
        temp_path.touch(exist_ok=True)
        
        temp_path.write_bytes(data)
        
        try:
            yield temp_path
        finally:
            temp_path.unlink(missing_ok=True)
