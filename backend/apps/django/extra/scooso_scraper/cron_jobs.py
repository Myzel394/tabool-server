import os
from multiprocessing import Pool

from django.contrib.auth import get_user_model

from apps.django.extra.scooso_scraper.jobs import fetch_timetable

__all__ = [
    "fetch_timetable_from_users"
]

User = get_user_model()


def fetch_timetable_from_users():
    users = User.objects.active_users().fetch_enabled().with_scooso_data()
    
    with Pool(os.cpu_count()) as pool:
        pool.map(fetch_timetable, users)
