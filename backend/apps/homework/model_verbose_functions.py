from django_common_utils.libraries.utils import model_verbose

from .model_references import *

__all__ = [
    "teacher_homework_single", "user_homework_single"
]


def teacher_homework_single():
    return model_verbose(TEACHER_HOMEWORK)


def user_homework_single():
    return model_verbose(USER_HOMEWORK)
