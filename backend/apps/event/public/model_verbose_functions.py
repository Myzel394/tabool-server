from django_common_utils.libraries.utils import model_verbose

from .model_references import *

__all__ = [
    "classtest_single", "event_single"
]


def classtest_single():
    return model_verbose(CLASSTEST)


def event_single():
    return model_verbose(EVENT)
