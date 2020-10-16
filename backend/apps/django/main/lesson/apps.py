from django.apps import AppConfig

from . import constants


class LessonConfig(AppConfig):
    name = "apps.django.main.lesson"
    app_label = constants.APP_LABEL
