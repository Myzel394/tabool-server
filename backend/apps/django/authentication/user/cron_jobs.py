from datetime import datetime

from django.contrib.auth import get_user_model

from apps.django.main.authentication.models import KnownIp

User = get_user_model()


def delete_known_ips():
    KnownIp.objects \
        .only("expire_date") \
        .filter(expire_date__lte=datetime.now()) \
        .delete()
