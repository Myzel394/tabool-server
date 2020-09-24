from django_common_utils.libraries.utils import model_verbose

from .model_references import *


def timetable_single():
    return model_verbose(TIMETABLE)
