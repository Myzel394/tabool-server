from django.urls import reverse
from django.http import HttpResponseForbidden
from django_hint import RequestType
from django.utils.translation import gettext_lazy as _


from .models import AccessToken


class EnsureAuthenticationToken:
    ALLOWED_URLS = {reverse("main:front_page")}
    COOKIE_NAME = "access_token"
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: RequestType):
        if request.path not in self.ALLOWED_URLS:
            if not self.is_request_valid(request):
                return HttpResponseForbidden(_("Zugangstoken fehlt oder nicht gültig!"))
        
        return self.get_response(request)
        
    def is_request_valid(self, request: RequestType) -> bool:
        try:
            access_token = request.COOKIES[self.COOKIE_NAME]
        except KeyError:
            return False

        return AccessToken.objects.only("id").get(id=access_token).exists()
