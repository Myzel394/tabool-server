from django_common_utils.libraries.utils import model_verbose

from .model_references import *


__all__ = [
    "course_single", "lesson_single", "lesson_data_single", "room_single", "subject_single",
    "teacher_single"
]


def course_single():
    return model_verbose(COURSE)


def lesson_single():
    return model_verbose(LESSON)


def lesson_data_single():
    return model_verbose(LESSON_DATA)


def room_single():
    return model_verbose(ROOM)


def subject_single():
    return model_verbose(SUBJECT)


def teacher_single():
    return model_verbose(TEACHER)
