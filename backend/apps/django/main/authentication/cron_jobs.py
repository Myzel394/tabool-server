from django.contrib.auth import get_user_model


def fetch_user_names():
    for user in get_user_model().objects.only("first_name").filter(first_name__isnull=True):
        user.scoosodata.fetch_user_data()
