from django.apps import AppConfig

from . import constants


class HomeworkConfig(AppConfig):
    name = 'apps.django.main.homework'
    app_label = constants.APP_LABEL
