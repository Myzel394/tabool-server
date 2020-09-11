from django.apps import AppConfig
from . import constants


class TimetableConfig(AppConfig):
    name = "apps.timetable"
    app_label = constants.APP_LABEL
