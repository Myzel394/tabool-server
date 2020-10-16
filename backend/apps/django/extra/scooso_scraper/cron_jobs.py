import os
from multiprocessing import Pool

from django.contrib.auth import get_user_model

from apps.django.extra.scooso_scraper.jobs import fetch_timetable

__all__ = [
    "fetch_timetable_from_users"
]


def fetch_timetable_from_users():
    users = get_user_model().objects.active_users().with_scooso_data()
    
    with Pool(os.cpu_count()) as pool:
        pool.map(fetch_timetable, users)
