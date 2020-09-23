from django.apps import AppConfig

from . import constants


class AuthenticationConfig(AppConfig):
    name = 'apps.authentication'
    app_label = constants.APP_LABEL
