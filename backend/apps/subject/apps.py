from django.apps import AppConfig

from . import constants


class SubjectConfig(AppConfig):
    name = "apps.subject"
    app_label = constants.APP_LABEL
