from datetime import datetime
from math import asin, cos, radians, sin, sqrt
from typing import *

import httpagentparser
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django_hint import RequestType
from requests import RequestException

from apps.django.authentication.otp.models import IPGeolocation
from apps.django.utils.request import get_client_ip
from . import constants

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User
    from .models import OTP

__all__ = [
    "haversine", "is_ip_geolocation_suspicious", "send_otp_message"
]

EARTH_RADIUS_IN_KILOMETERS = 6371


# https://stackoverflow.com/a/4913653/9878135
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:  # pragma: no cover
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return c * EARTH_RADIUS_IN_KILOMETERS


def fetch_location(ip: str) -> Optional[tuple[str, str, str]]:
    try:
        url = f"https://api.ipgeolocationapi.com/geolocate/{ip}"
        response = requests.get(url)

        if 400 <= response.status_code < 600:
            return

        data = response.json()
        geo_data = data["geo"]
        longitude = geo_data["longitude"]
        latitude = geo_data["latitude"]
        city = data["name"]
    except (
            RequestException,  # request
            ValueError,  # .json()
            KeyError,  # data
    ):
        return None
    else:
        return longitude, latitude, city


def get_ip_location(ip: str) -> Optional[IPGeolocation]:
    try:
        ip_location = IPGeolocation.objects.only("ip_address").get(ip_address=ip)
    except ObjectDoesNotExist:
        # Fetch new location
        if location := fetch_location(ip):
            longitude, latitude, city = location

            ip_location = IPGeolocation.objects.create(
                longitude=longitude,
                latitude=latitude,
                ip_address=ip,
                city=city
            )

            return ip_location
    else:
        return ip_location

    return


def is_ip_geolocation_suspicious(ip: str) -> bool:
    if settings.DEBUG and ip == "127.0.0.1":
        return False

    if ip_location := get_ip_location(ip):
        longitude = ip_location.longitude
        latitude = ip_location.latitude

        radius = abs(haversine(longitude, latitude, *constants.VALID_LOGIN_LOCATION))

        if radius <= constants.VALID_LOGIN_LOCATION_RADIUS:
            return False

    return True


def send_otp_message(request: RequestType, user: "User", otp: "OTP"):
    now = datetime.now()
    ip = get_client_ip(request)

    # Create message
    message_parts = [
        f"Ip: {ip}"
    ]

    try:
        ip_location = get_ip_location(ip)

        if ip_location:
            message_parts.append(
                f"Ort: {ip_location.city or '-'} ({ip_location.longitude} Long, {ip_location.latitude} Lat)"
            )
        else:
            message_parts.append("Ort: Unbekannt")
    # A general exception is used, to ensure that the user will at least get some information
    except Exception:  # skipcq: FLK-E722
        pass

    try:
        os, browser = httpagentparser.simple_detect(request["HTTP_USER_AGENT"])

        message_parts.append(f"Browser: {browser} auf einem {os} Gerät")
    except:  # skipcq: FLK-E722
        pass

    message_information = "\n".join(message_parts)

    message = f"""
    Hi {user.first_name}!

    Es gab eine neue Anmeldung gegen am {now.strftime('%d.%m.%Y %H:%M:%S')}.
    
    Wenn diese Anmeldung von dir ist, gib diesen Code ein:
        {otp.token}
        
    
    Informationen über die Anmeldung:
    {message_information}
    """

    send_mail(
        "Neue Anmeldung. Hier dein Code.",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
