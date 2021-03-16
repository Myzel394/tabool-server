import random
import string

import names
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

# noinspection PyUnresolvedReferences
from apps.django.extra.news.models import *
from apps.django.extra.scooso_scraper.actions import fetch_timetable, import_teachers
from apps.django.main.authentication.models import *
# noinspection PyUnresolvedReferences
from apps.django.main.event.models import *
# noinspection PyUnresolvedReferences
from apps.django.main.homework.models import *
# noinspection PyUnresolvedReferences
from apps.django.main.lesson.models import *
# noinspection PyUnresolvedReferences
from apps.django.main.school_data.models import *


def get_set_values(model, field):
    return set(model.objects.all().values_list(field, flat=True))


def create_user(confirm: bool = True, scooso_data: bool = True, staff: bool = False):
    load_dotenv()
    User = get_user_model()
    
    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    
    user = User.objects.create_user(
        email=f"{names.get_first_name()}@gmail.com",
        password=password
    )
    
    if confirm:
        user.confirm_email(user.confirmation_key)
    if scooso_data:
        user_scooso_data = ScoosoData.objects.create(
            user=user,
            username=os.getenv("SCOOSO_USERNAME", "username"),
            password=os.getenv("SCOOSO_PASSWORD", "password")
        )
    if staff:
        user.is_superuser = True
        user.is_staff = True
    
    user.save()
    
    print("Email:", user.email)
    print("Password:", password)
    
    return user


def load_dummy_user():
    load_dotenv()
    load_dotenv(settings.BASE_DIR / ".." / "scooso_data.env")
    print("Fetching teachers")
    import_teachers()
    
    print("Creating user")
    
    print(os.getenv("SCOOSO_USERNAME", ))
    teacher = Teacher.objects.create(
        first_name="FirstName",
        last_name="LastName",
        short_name="SHN"
    )
    student = create_user(staff=True, scooso_data=True)
    Student.objects.create(
        main_teacher=teacher,
        class_number=8,
        user=student,
    )
    
    print("Fetching timetable")
    fetch_timetable(student, in_thread=False)
    print("=" * 20 + " Done! " + "=" * 20)
