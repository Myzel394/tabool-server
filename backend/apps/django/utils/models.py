import secrets
import string

from django.db import models
from django_lifecycle import LifecycleModel

from apps.django.authentication.user.public import *
from apps.django.authentication.user.public import model_names as auth_names

__all__ = [
    "AssociatedUserMixin", "UserModelRelationMixin", "IdMixin"
]


class AssociatedUserMixin(models.Model):
    class Meta:
        abstract = True
    
    associated_user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name=auth_names.USER
    )


class UserModelRelationMixin(models.Model):
    class Meta:
        abstract = True
    
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name=auth_names.USER
    )


class IdMixin(LifecycleModel):
    class Meta:
        abstract = True
    
    ID_LENGTH = 8
    
    id = models.CharField(
        max_length=ID_LENGTH,
        unique=True,
        primary_key=True
    )
    
    def save(self, *args, **kwargs):
        if self.id is None or self.id == "":
            available_ids = set(self.__class__.objects.all().values_list("id", flat=True))
            
            while True:
                object_id = "".join(
                    secrets.choice(string.ascii_letters + string.digits)
                    for _ in range(self.ID_LENGTH)
                )
                
                if object_id not in available_ids:
                    break
            
            self.id = object_id
        
        return super().save(*args, **kwargs)
