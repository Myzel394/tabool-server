from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

urlpatterns = [
    url(r"", AsgiHandler)
]

application = ProtocolTypeRouter({
    "http": URLRouter(urlpatterns)
})
