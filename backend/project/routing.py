from channels.routing import ProtocolTypeRouter, URLRouter

import apps.event.routing

application = ProtocolTypeRouter({
    "http": URLRouter(apps.event.routing.urlpatterns)
})
