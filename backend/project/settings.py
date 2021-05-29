from .base_settings import *

DEBUG = False

load_dotenv("prod.env")

CRONJOBS = [
    (os.getenv("CRON_DELETE_KNOWN_IPS", "* * * * *"), "apps.django.core.authentication.delete_known_ips")
]
CRONTAB_LOCK_JOBS = True
