from django.apps import AppConfig

from . import constants


class OtpConfig(AppConfig):
    name = 'apps.django.main.otp'
    app_label = constants.APP_LABEL
