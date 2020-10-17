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
    
    
    # TODO: Add flush function (flush function should delete all objects!)
    
    def create_user(confirm: bool = True, scooso_data: bool = True):
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
        
        print("Email:", user.email)
        print("Password:", password)
        
        return user
