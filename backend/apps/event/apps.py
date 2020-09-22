from django.apps import AppConfig

from . import constants


class EventsConfig(AppConfig):
    name = "apps.event"
    app_label = constants.APP_LABEL
