from django.apps import AppConfig

app_name = "session"


class SessionsConfig(AppConfig):
    name = 'apps.django.authentication.sessions'
    app_label = "session"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
