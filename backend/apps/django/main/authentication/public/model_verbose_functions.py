from django_common_utils.libraries.utils import model_verbose

from .model_references import *


def access_token_single():
    return model_verbose(ACCESS_TOKEN)


def user_single():
    return model_verbose(USER)
