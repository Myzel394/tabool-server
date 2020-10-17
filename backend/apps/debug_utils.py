from django.conf import settings
from django.contrib.auth import get_user_model

if settings.DEBUG:
    from dotenv import load_dotenv
    import random, string, names, os
    
    from apps.django.main.authentication.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.event.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.lesson.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.homework.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.school_data.models import *
    # noinspection PyUnresolvedReferences
    from apps.django.main.news.models import *
    
    
    def flush():
        for model in [Room, Subject, Teacher, Course, Event, News, User]:
            print(f"Deleting {model.__class__.__name__.lower()}s")
            model.objects.all().delete()
    
    
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
                username=os.getenv("SCOOSO_USERNAME"),
                password=os.getenv("SCOOSO_PASSWORD")
            )
        if staff:
            user.is_superuser = True
            user.is_staff = True
        
        user.save()
        
        print("Email:", user.email)
        print("Password:", password)
        
        return user
