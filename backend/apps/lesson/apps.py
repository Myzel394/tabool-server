from django.apps import AppConfig

from . import constants


class LessonConfig(AppConfig):
    name = "apps.lesson"
    app_label = constants.APP_LABEL
