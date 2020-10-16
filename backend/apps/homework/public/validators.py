from secure_file_detection.constants import SUPPORTED_MIMETYPES

from apps.utils.fields import SafeFileValidator

__all__ = [
    "safe_file_validator"
]


def safe_file_validator(*args, **kwargs):
    return SafeFileValidator(SUPPORTED_MIMETYPES)(*args, **kwargs)
