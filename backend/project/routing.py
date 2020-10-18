import django_eventstream
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from apps.django.extra.news.public import NEWS_CHANNEL
from apps.django.main.authentication.public import USER_NAMES_FETCHED_CHANNEL
from apps.django.main.event.public import MODIFICATION_CHANNEL
from apps.django.main.homework.public import HOMEWORK_CHANNEL

urlpatterns = [
    url(
        r"^events/",
        AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ),
        {"channels": [MODIFICATION_CHANNEL, HOMEWORK_CHANNEL, NEWS_CHANNEL, USER_NAMES_FETCHED_CHANNEL]}
    ),
    url(r"", AsgiHandler)
]

application = ProtocolTypeRouter({
    "http": URLRouter(urlpatterns)
})
