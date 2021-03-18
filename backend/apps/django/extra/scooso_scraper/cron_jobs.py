import os
from datetime import datetime, timedelta
from multiprocessing import Pool

from django.contrib.auth import get_user_model

from .jobs import fetch_timetable
from .models import ScoosoRequest

__all__ = [
    "fetch_timetable_from_users"
]

User = get_user_model()


def fetch_timetable_from_users():
    users = User.objects.active_users().fetch_enabled().with_scooso_data()
    
    with Pool(os.cpu_count()) as pool:
        pool.map(fetch_timetable, users)


def delete_old_requests():
    expire_date = datetime.now() - timedelta(days=ScoosoRequest.EXPIRE_DAYS)
    
    ScoosoRequest.objects.only("created_at").filter(created_at__lte=expire_date).delete()
