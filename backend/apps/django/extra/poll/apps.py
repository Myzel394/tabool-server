from django.apps import AppConfig

from .constants import APP_LABEL


class PollConfig(AppConfig):
    name = 'apps.django.extra.poll'
    app_label = APP_LABEL
