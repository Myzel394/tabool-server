from django.conf import settings

from apps.django.core.utils import remove_empty_folders


def cleanup_lib_dir():
    remove_empty_folders(settings.LIB_DIR)
