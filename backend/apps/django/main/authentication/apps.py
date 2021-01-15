from django.apps import AppConfig

from . import constants


class AuthenticationConfig(AppConfig):
    name = "apps.django.main.authentication"
    app_label = constants.APP_LABEL
    
    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
