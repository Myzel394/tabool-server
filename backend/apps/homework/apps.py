from django.apps import AppConfig

from . import constants


class HomeworkConfig(AppConfig):
    name = 'apps.homework'
    app_label = constants.APP_LABEL
    
    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
