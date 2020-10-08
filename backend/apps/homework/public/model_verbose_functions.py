from django_common_utils.libraries.utils import model_verbose

from .model_references import *

__all__ = [
    "homework_single", "material_single"
]


def homework_single():
    return model_verbose(HOMEWORK)


def material_single():
    return model_verbose(MATERIAL)
