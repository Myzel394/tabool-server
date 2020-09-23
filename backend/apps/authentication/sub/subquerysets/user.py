from django_common_utils.libraries.models import CustomQuerySetMixin
from django.utils.translation import gettext_lazy as _


class UserQuerySet(CustomQuerySetMixin.QuerySet):
    def create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError(_("Email nicht angegeben."))
        email = self.normalize_email()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
        
    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_staff=True and is_superuser=True"))
        
        return self.create_user(email, password, **extra_fields)

