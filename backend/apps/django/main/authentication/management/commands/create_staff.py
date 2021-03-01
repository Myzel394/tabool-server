import random
import string

import names
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Creates a staff user"
    
    def handle(self, *args, **options):
        User = get_user_model()
        
        password = "".join(random.choices(string.ascii_letters + string.digits, k=8))  # nosec
        
        user = User.objects.create_user(
            email=f"{names.get_first_name()}@gmail.com",
            password=password,
            is_superuser=True,
            is_staff=True
        )
        
        print("Email:", user.email)
        print("Password:", password)
        
        return user
