from django.apps import AppConfig

from . import constants


class EventConfig(AppConfig):
    name = "apps.event"
    app_label = constants.APP_LABEL
