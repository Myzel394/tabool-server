from datetime import datetime

from django.contrib.auth import get_user_model

from apps.django.main.authentication.models import KnownIp

User = get_user_model()


def fetch_user_names():
    for user in User.objects.fetch_enabled().with_scooso_data():
        user.scoosodata.fetch_user_data()


def delete_known_ips():
    KnownIp.objects \
        .only("expire_date") \
        .filter(expire_date__lte=datetime.now()) \
        .delete()
