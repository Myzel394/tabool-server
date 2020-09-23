from django.conf import settings
from django_common_utils.libraries.utils import model_verbose


def user_single():
    return model_verbose(settings.AUTH_USER_MODEL)

