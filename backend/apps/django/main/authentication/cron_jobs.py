from datetime import datetime

from django.contrib.auth import get_user_model

from apps.django.main.authentication.models import KnownIp


def fetch_user_names():
    for user in get_user_model().objects.only("first_name").filter(first_name__isnull=True):
        user.scoosodata.fetch_user_data()


def delete_known_ips():
    KnownIp.objects \
        .only("expire_date") \
        .filter(expire_date__lte=datetime.now()) \
        .delete()
