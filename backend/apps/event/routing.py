import django_eventstream
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import URLRouter
from django.conf.urls import url

from .public import *

__all__ = [
    "urlpatterns"
]

# TODO: Change url!
urlpatterns = [
    url(
        r"^events/modification/",
        AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ),
        {"channels": [MODIFICATION_CHANNEL]}
    ),
    url(r"", AsgiHandler)
]
