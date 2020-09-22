from django_common_utils.libraries.utils import model_verbose

from .model_references import *

__all__ = [
    "class_test_single", "event_single", "event_user_option_single"
]


def class_test_single():
    return model_verbose(CLASS_TEST)


def event_single():
    return model_verbose(EVENT)


def event_user_option_single():
    return model_verbose(EVENT_USER_OPTION)
