from django.apps import AppConfig

from . import constants


class UserConfig(AppConfig):
    name = "apps.django.authentication.user"
    app_label = constants.APP_LABEL
    
    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
